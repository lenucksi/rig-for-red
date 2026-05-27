from __future__ import annotations

import asyncio
import logging
import time as _time
from collections.abc import Callable
from datetime import datetime, time, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import (
    async_track_point_in_time,
    async_track_state_change_event,
    async_track_time_change,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import (
    CONF_ADAPTIVE_LIGHTING_SWITCHES,
    CONF_DIM_DURATION_MINUTES,
    CONF_ENABLE_DEBUG_LOGGING,
    CONF_LIGHTS,
    CONF_MIN_BRIGHTNESS_PCT,
    CONF_RESTORE_AT_SUNRISE,
    CONF_RESTORE_TIME,
    CONF_SCHEDULE_DAYS,
    CONF_SCHEDULE_TIME,
    DEFAULT_DIM_DURATION_MINUTES,
    DEFAULT_ENABLE_DEBUG_LOGGING,
    DEFAULT_MIN_BRIGHTNESS_PCT,
    DEFAULT_RESTORE_AT_SUNRISE,
    DIM_STEPS,
    DOMAIN,
    RED_RGB,
    WHITE_COLOR_TEMP_KELVIN,
)

_LOGGER = logging.getLogger(__name__)


def _parse_time(value: str | time | None) -> time | None:
    if value is None:
        return None
    if isinstance(value, time):
        return value
    try:
        parts = value.split(":")
        return time(int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return None


class RigForRedCoordinator(DataUpdateCoordinator[None]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(hass, _LOGGER, name=DOMAIN)

        data = entry.data

        _LOGGER.debug(
            "RigForRedCoordinator.__init__: entry_id=%s, lights=%s, schedule_days=%s, schedule_time=%s, "
            "dim_duration=%s, restore_at_sunrise=%s, restore_time=%s, al_switches=%s, "
            "min_brightness_pct=%s, enable_debug_logging=%s",
            entry.entry_id,
            data.get(CONF_LIGHTS),
            data.get(CONF_SCHEDULE_DAYS),
            data.get(CONF_SCHEDULE_TIME),
            data.get(CONF_DIM_DURATION_MINUTES, DEFAULT_DIM_DURATION_MINUTES),
            data.get(CONF_RESTORE_AT_SUNRISE, DEFAULT_RESTORE_AT_SUNRISE),
            data.get(CONF_RESTORE_TIME),
            data.get(CONF_ADAPTIVE_LIGHTING_SWITCHES),
            data.get(CONF_MIN_BRIGHTNESS_PCT, DEFAULT_MIN_BRIGHTNESS_PCT),
            data.get(CONF_ENABLE_DEBUG_LOGGING, DEFAULT_ENABLE_DEBUG_LOGGING),
        )

        self._lights: list[str] = data.get(CONF_LIGHTS, [])
        self._schedule_days: list[str] = data.get(CONF_SCHEDULE_DAYS, [])
        self._schedule_time: time | None = _parse_time(data.get(CONF_SCHEDULE_TIME))
        dim_default = DEFAULT_DIM_DURATION_MINUTES
        self._dim_duration: int = data.get(CONF_DIM_DURATION_MINUTES, dim_default)
        restore_default = DEFAULT_RESTORE_AT_SUNRISE
        self._restore_at_sunrise: bool = data.get(CONF_RESTORE_AT_SUNRISE, restore_default)
        self._restore_time: time | None = _parse_time(data.get(CONF_RESTORE_TIME))
        self._al_switches: list[str] = data.get(CONF_ADAPTIVE_LIGHTING_SWITCHES, [])
        min_brightness_default = DEFAULT_MIN_BRIGHTNESS_PCT
        self._min_brightness_pct: int = data.get(CONF_MIN_BRIGHTNESS_PCT, min_brightness_default)
        self._enable_debug_logging: bool = data.get(CONF_ENABLE_DEBUG_LOGGING, DEFAULT_ENABLE_DEBUG_LOGGING)

        self._unsub_schedule: Callable[[], None] | None = None
        self._unsub_restore: Callable[[], None] | None = None
        self._unsub_sunrise: Callable[[], None] | None = None
        self._is_active = False
        self._dim_task: asyncio.Task | None = None

        self._lights_to_restore: list[str] = []
        self._lights_waiting_for_red: list[str] = []
        self._light_state_unsubs: list[Callable] = []

    @property
    def is_active(self) -> bool:
        return self._is_active

    async def async_setup(self) -> None:
        if self._enable_debug_logging:
            _LOGGER.setLevel(logging.DEBUG)
            _LOGGER.debug("Debug logging enabled via config option")

        if self._schedule_time is not None:
            self._unsub_schedule = async_track_time_change(
                self.hass,
                self._schedule_trigger,
                hour=self._schedule_time.hour,
                minute=self._schedule_time.minute,
                second=self._schedule_time.second,
            )

        if not self._restore_at_sunrise and self._restore_time is not None:
            self._unsub_restore = async_track_time_change(
                self.hass,
                self._restore_trigger,
                hour=self._restore_time.hour,
                minute=self._restore_time.minute,
                second=self._restore_time.second,
            )

        _LOGGER.info(
            "Rig-for-Red setup complete: schedule=%s (%s), restore=%s",
            self._schedule_time,
            self._schedule_days,
            "sunrise" if self._restore_at_sunrise else self._restore_time,
        )

    async def async_unload(self) -> None:
        _LOGGER.debug("Unloading Rig-for-Red coordinator")
        if self._unsub_schedule is not None:
            self._unsub_schedule()
            self._unsub_schedule = None

        if self._unsub_restore is not None:
            self._unsub_restore()
            self._unsub_restore = None

        if self._unsub_sunrise is not None:
            self._unsub_sunrise()
            self._unsub_sunrise = None

        for unsub in self._light_state_unsubs:
            unsub()
        self._light_state_unsubs = []

        if self._dim_task is not None and not self._dim_task.done():
            self._dim_task.cancel()
            self._dim_task = None

    async def _schedule_trigger(self, now: datetime) -> None:
        day_abbr = now.strftime("%a").lower()
        _LOGGER.info(
            "Schedule triggered at %s: day=%s, schedule_days=%s, day_ok=%s, active=%s",
            now,
            day_abbr,
            self._schedule_days,
            day_abbr in self._schedule_days,
            self._is_active,
        )
        if day_abbr not in self._schedule_days:
            return
        if self._is_active:
            return
        _LOGGER.info("Starting activation sequence")
        self.hass.async_create_task(self.async_activate())

    async def _restore_trigger(self, _now) -> None:
        _LOGGER.info("Restore trigger fired at %s", _now)
        self.hass.async_create_task(self.async_restore())

    async def _get_next_sunrise(self) -> datetime:
        sun_state = self.hass.states.get("sun.sun")
        if sun_state and "next_rising" in sun_state.attributes:
            next_rising = dt_util.parse_datetime(sun_state.attributes["next_rising"])
            if next_rising is not None:
                _LOGGER.debug("Next sunrise: %s", next_rising)
                return next_rising
        fallback = dt_util.utcnow() + timedelta(hours=8)
        _LOGGER.warning("Sun state not available, using fallback sunrise: %s", fallback)
        return fallback

    async def _disable_al_switches(self) -> None:
        if not self._al_switches:
            return
        _LOGGER.info("Disabling %d Adaptive Lighting switch(es): %s", len(self._al_switches), self._al_switches)
        for switch in self._al_switches:
            try:
                _LOGGER.debug("set_manual_control(switch=%s, manual_control=True)", switch)
                t_before = _time.monotonic()
                await self.hass.services.async_call(
                    "adaptive_lighting",
                    "set_manual_control",
                    {
                        "entity_id": switch,
                        "lights": self._lights,
                        "manual_control": True,
                    },
                    blocking=True,
                )
                _LOGGER.debug("set_manual_control(%s) took %.2fs", switch, _time.monotonic() - t_before)
            except Exception:  # noqa: BLE001
                _LOGGER.warning("Failed to set manual control for AL switch %s", switch)
            try:
                _LOGGER.debug("Turning off AL switch %s", switch)
                t_before = _time.monotonic()
                await self.hass.services.async_call(
                    "switch",
                    "turn_off",
                    {"entity_id": switch},
                    blocking=True,
                )
                _LOGGER.debug("switch.turn_off(%s) took %.2fs", switch, _time.monotonic() - t_before)
            except Exception:  # noqa: BLE001
                _LOGGER.warning("Failed to turn off AL switch %s", switch)

    async def async_activate(self) -> None:
        _LOGGER.info("Activation started at %s", dt_util.utcnow())
        if self._is_active:
            _LOGGER.debug("Already active, skipping activation")
            return

        await self._disable_al_switches()

        await asyncio.sleep(0.5)

        on_lights = []
        off_lights = []
        for entity_id in self._lights:
            state = self.hass.states.get(entity_id)
            is_on = state is not None and state.state == "on"
            brightness = state.attributes.get("brightness") if is_on else None
            color = (state.attributes.get("rgb_color") or state.attributes.get("color_temp_kelvin")) if is_on else None
            _LOGGER.debug(
                "Light '%s': state=%s, brightness=%s, color=%s",
                entity_id,
                state.state if state else "unknown",
                brightness,
                color,
            )
            if is_on:
                on_lights.append(entity_id)
            elif state is not None and state.state == "off":
                off_lights.append(entity_id)

        _LOGGER.info(
            "Light check: %d on, %d off, %d unavail",
            len(on_lights),
            len(off_lights),
            len(self._lights) - len(on_lights) - len(off_lights),
        )

        if not on_lights:
            _LOGGER.info("No lights are on, entering standby mode - will apply red on next turn_on")
            return

        start_brightness = 255
        for light in on_lights:
            state = self.hass.states.get(light)
            if state is not None:
                brightness = state.attributes.get("brightness", 255)
                if brightness > start_brightness:
                    start_brightness = brightness

        _LOGGER.info("Setting %d active lights to red at brightness=%s", len(on_lights), start_brightness)
        t_before = _time.monotonic()
        await self.hass.services.async_call(
            "light",
            "turn_on",
            {"entity_id": on_lights, "rgb_color": RED_RGB, "brightness": start_brightness},
            blocking=True,
        )
        _LOGGER.debug("light.turn_on(red) for %d lights took %.2fs", len(on_lights), _time.monotonic() - t_before)

        self._lights_to_restore = list(on_lights)
        self._lights_waiting_for_red = list(off_lights)
        dim_interval = (self._dim_duration * 60) / DIM_STEPS
        _LOGGER.info(
            "Starting staged dimming: %d steps, %d min, interval=%.1fs",
            DIM_STEPS,
            self._dim_duration,
            dim_interval,
        )
        self._dim_task = asyncio.create_task(self._dim_lights(start_brightness))

        _LOGGER.debug("Registering state change listeners for %d lights", len(on_lights) + len(off_lights))
        for entity_id in on_lights + off_lights:
            unsub = async_track_state_change_event(
                self.hass,
                [entity_id],
                self._on_tracked_light_change,
            )
            self._light_state_unsubs.append(unsub)

        if self._restore_at_sunrise:
            next_sunrise = await self._get_next_sunrise()
            _LOGGER.debug("Scheduling sunrise restore at %s", next_sunrise)
            self._unsub_sunrise = async_track_point_in_time(
                self.hass,
                self._restore_trigger,
                next_sunrise,
            )

        self._is_active = True
        _LOGGER.info("Rig-for-Red activation complete")
        self.async_set_updated_data({"is_active": True})

    async def _re_enable_al_switches(self) -> None:
        if not self._al_switches:
            return
        _LOGGER.info("Re-enabling %d Adaptive Lighting switch(es): %s", len(self._al_switches), self._al_switches)
        for switch in self._al_switches:
            try:
                _LOGGER.debug("set_manual_control(switch=%s, manual_control=False)", switch)
                t_before = _time.monotonic()
                await self.hass.services.async_call(
                    "adaptive_lighting",
                    "set_manual_control",
                    {
                        "entity_id": switch,
                        "lights": self._lights,
                        "manual_control": False,
                    },
                    blocking=True,
                )
                _LOGGER.debug("set_manual_control(%s) took %.2fs", switch, _time.monotonic() - t_before)
            except Exception:  # noqa: BLE001
                _LOGGER.warning("Failed to set manual control for AL switch %s", switch)
            try:
                _LOGGER.debug("Turning on AL switch %s", switch)
                t_before = _time.monotonic()
                await self.hass.services.async_call(
                    "switch",
                    "turn_on",
                    {"entity_id": switch},
                    blocking=True,
                )
                _LOGGER.debug("switch.turn_on(%s) took %.2fs", switch, _time.monotonic() - t_before)
            except Exception:  # noqa: BLE001
                _LOGGER.warning("Failed to turn on AL switch %s", switch)

    async def async_restore(self) -> None:
        _LOGGER.info("Restore started at %s", dt_util.utcnow())

        for unsub in self._light_state_unsubs:
            unsub()
        self._light_state_unsubs = []
        self._lights_waiting_for_red = []

        if self._dim_task is not None and not self._dim_task.done():
            _LOGGER.debug("Cancelling dim task")
            self._dim_task.cancel()
            await asyncio.gather(self._dim_task, return_exceptions=True)
            self._dim_task = None

        self._is_active = False

        if self._lights_to_restore:
            _LOGGER.info("Restoring %d lights to white (2700K, 100%%)", len(self._lights_to_restore))
            t_before = _time.monotonic()
            await self.hass.services.async_call(
                "light",
                "turn_on",
                {
                    "entity_id": self._lights_to_restore,
                    "color_temp_kelvin": WHITE_COLOR_TEMP_KELVIN,
                    "brightness": 255,
                    "transition": 2,
                },
                blocking=True,
            )
            _LOGGER.debug(
                "light.turn_on(white) for %d lights took %.2fs",
                len(self._lights_to_restore),
                _time.monotonic() - t_before,
            )
        else:
            _LOGGER.debug("No lights to restore (all were turned off by user)")
        self._lights_to_restore = []

        await self._re_enable_al_switches()

        if self._restore_at_sunrise and self._unsub_sunrise is not None:
            self._unsub_sunrise()
            self._unsub_sunrise = None

    async def _dim_lights(self, start_brightness: int) -> None:
        target = max(1, int(self._min_brightness_pct / 100 * 255))
        interval = (self._dim_duration * 60) / DIM_STEPS
        _LOGGER.debug(
            "Dim task started: start=%s, target=%s, steps=%s, interval=%.1fs",
            start_brightness,
            target,
            DIM_STEPS,
            interval,
        )
        for i in range(1, DIM_STEPS + 1):
            if not self._is_active:
                _LOGGER.debug("Dim task cancelled (inactive) at step %d/%d", i, DIM_STEPS)
                return
            brightness = int(start_brightness - (start_brightness - target) * i / DIM_STEPS)
            currently_on = [e for e in self._lights_to_restore if self._light_is_on(e)]
            prev_brightness = (
                start_brightness
                if i == 1
                else int(
                    start_brightness - (start_brightness - target) * (i - 1) / DIM_STEPS,
                )
            )
            _LOGGER.debug(
                "Dim step %d/%d: brightness %d->%d (%d lights: %s)",
                i,
                DIM_STEPS,
                prev_brightness,
                brightness,
                len(currently_on),
                currently_on,
            )
            if not currently_on:
                _LOGGER.debug("Dim step %d/%d: no lights on, sleeping %.1fs", i, DIM_STEPS, interval)
                await asyncio.sleep(interval)
                continue
            t_before = _time.monotonic()
            await self.hass.services.async_call(
                "light",
                "turn_on",
                {
                    "entity_id": currently_on,
                    "rgb_color": RED_RGB,
                    "brightness": max(1, brightness),
                    "transition": interval,
                },
                blocking=True,
            )
            zigbee_latency = _time.monotonic() - t_before
            _LOGGER.debug(
                "Dim step %d/%d: light.turn_on took %.2fs (Zigbee latency)",
                i,
                DIM_STEPS,
                zigbee_latency,
            )
            try:
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                _LOGGER.debug("Dim task cancelled at step %d/%d", i, DIM_STEPS)
                return

    def _light_is_on(self, entity_id: str) -> bool:
        state = self.hass.states.get(entity_id)
        return state is not None and state.state == "on"

    async def _is_restore_imminent(self) -> bool:
        now = dt_util.utcnow()
        if self._restore_at_sunrise:
            next_sunrise = await self._get_next_sunrise()
            seconds_until = (next_sunrise - now).total_seconds()
            if 0 <= seconds_until <= 600:
                _LOGGER.debug("Restore imminent: sunrise in %.0fs", seconds_until)
                return True
        if self._restore_time is not None:
            restore_dt = dt_util.as_utc(datetime.combine(now.date(), self._restore_time))
            if restore_dt < now:
                restore_dt += timedelta(days=1)
            seconds_until = (restore_dt - now).total_seconds()
            if 0 <= seconds_until <= 600:
                _LOGGER.debug("Restore imminent: restore_time in %.0fs", seconds_until)
                return True
        return False

    async def _on_tracked_light_change(self, event) -> None:
        entity_id = event.data["entity_id"]
        new_state = event.data.get("new_state")
        old_state = event.data.get("old_state")

        if new_state is None or old_state is None:
            return

        if old_state.state == "off" and new_state.state == "on" and entity_id in self._lights_waiting_for_red:
            _LOGGER.info("Light '%s' turned ON during night mode", entity_id)
            self._lights_waiting_for_red.remove(entity_id)
            if entity_id not in self._lights_to_restore:
                self._lights_to_restore.append(entity_id)
            if await self._is_restore_imminent():
                _LOGGER.debug("Not setting '%s' to red, restore is imminent", entity_id)
                return
            _LOGGER.debug("Setting '%s' to red (was off at activation)", entity_id)
            t_before = _time.monotonic()
            await self.hass.services.async_call(
                "light",
                "turn_on",
                {"entity_id": entity_id, "rgb_color": RED_RGB},
                blocking=False,
            )
            _LOGGER.debug("light.turn_on(%s, red) took %.2fs", entity_id, _time.monotonic() - t_before)

        if old_state.state == "on" and new_state.state == "off" and entity_id in self._lights_to_restore:
            _LOGGER.info("Light '%s' turned OFF during night mode, removed from restore list", entity_id)
            self._lights_to_restore.remove(entity_id)
            next_sunrise = await self._get_next_sunrise()
            _LOGGER.debug("Re-registering sunrise listener for next restore at %s", next_sunrise)
            self._unsub_sunrise = async_track_point_in_time(
                self.hass,
                self._restore_trigger,
                next_sunrise,
            )

        _LOGGER.info("Rig-for-Red restore complete")
        self.async_set_updated_data({"is_active": False})
