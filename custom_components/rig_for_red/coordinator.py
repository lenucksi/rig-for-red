from __future__ import annotations

import asyncio
import logging
from datetime import datetime, time, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_point_in_time, async_track_time_change
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import (
    CONF_ADAPTIVE_LIGHTING_SWITCHES,
    CONF_DIM_DURATION_MINUTES,
    CONF_LIGHTS,
    CONF_MIN_BRIGHTNESS_PCT,
    CONF_RESTORE_AT_SUNRISE,
    CONF_RESTORE_TIME,
    CONF_SCHEDULE_DAYS,
    CONF_SCHEDULE_TIME,
    DEFAULT_DIM_DURATION_MINUTES,
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

        self._unsub_schedule = None
        self._unsub_restore = None
        self._unsub_sunrise = None
        self._is_active = False
        self._dim_task = None

    @property
    def is_active(self) -> bool:
        return self._is_active

    async def async_setup(self) -> None:
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

    async def async_unload(self) -> None:
        if self._unsub_schedule is not None:
            self._unsub_schedule()
            self._unsub_schedule = None

        if self._unsub_restore is not None:
            self._unsub_restore()
            self._unsub_restore = None

        if self._unsub_sunrise is not None:
            self._unsub_sunrise()
            self._unsub_sunrise = None

        if self._dim_task is not None and not self._dim_task.done():
            self._dim_task.cancel()
            self._dim_task = None

    async def _schedule_trigger(self, now: datetime) -> None:
        day_abbr = now.strftime("%a").lower()
        if day_abbr not in self._schedule_days:
            return
        if self._is_active:
            return
        self.hass.async_create_task(self.async_activate())

    async def _restore_trigger(self, now) -> None:
        self.hass.async_create_task(self.async_restore())

    async def _get_next_sunrise(self) -> datetime:
        sun_state = self.hass.states.get("sun.sun")
        if sun_state and "next_rising" in sun_state.attributes:
            next_rising = dt_util.parse_datetime(sun_state.attributes["next_rising"])
            if next_rising is not None:
                return next_rising
        return dt_util.utcnow() + timedelta(hours=8)

    async def async_activate(self) -> None:
        if self._is_active:
            return

        for switch in self._al_switches:
            try:
                await self.hass.services.async_call(
                    "switch",
                    "turn_off",
                    {"entity_id": switch},
                    blocking=True,
                )
            except Exception:
                _LOGGER.exception("Failed to turn off AL switch %s", switch)
            try:
                await self.hass.services.async_call(
                    "switch",
                    "set_manual_control",
                    {"entity_id": switch, "manual_control": True},
                    blocking=True,
                )
            except Exception:
                _LOGGER.exception("Failed to set manual control for AL switch %s", switch)

        start_brightness = 255
        for light in self._lights:
            state = self.hass.states.get(light)
            if state is not None:
                brightness = state.attributes.get("brightness", 255)
                if brightness > start_brightness:
                    start_brightness = brightness

        await self.hass.services.async_call(
            "light",
            "turn_on",
            {"entity_id": self._lights, "rgb_color": RED_RGB, "brightness": start_brightness},
            blocking=True,
        )

        self._dim_task = asyncio.create_task(self._dim_lights(start_brightness))

        if self._restore_at_sunrise:
            next_sunrise = await self._get_next_sunrise()
            self._unsub_sunrise = async_track_point_in_time(
                self.hass, self._restore_trigger, next_sunrise
            )

        self._is_active = True
        self.async_set_updated_data({"is_active": True})

    async def async_restore(self) -> None:
        if self._dim_task is not None and not self._dim_task.done():
            self._dim_task.cancel()
            await asyncio.gather(self._dim_task, return_exceptions=True)
            self._dim_task = None

        self._is_active = False

        await self.hass.services.async_call(
            "light",
            "turn_on",
            {
                "entity_id": self._lights,
                "color_temp_kelvin": WHITE_COLOR_TEMP_KELVIN,
                "brightness": 255,
                "transition": 2,
            },
            blocking=True,
        )

        for switch in self._al_switches:
            try:
                await self.hass.services.async_call(
                    "switch", "turn_on", {"entity_id": switch}, blocking=True
                )
            except Exception:
                _LOGGER.exception("Failed to turn on AL switch %s", switch)
            try:
                await self.hass.services.async_call(
                    "switch",
                    "set_manual_control",
                    {"entity_id": switch, "manual_control": False},
                    blocking=True,
                )
            except Exception:
                _LOGGER.exception(
                    "Failed to set manual control for AL switch %s", switch
                )

        if self._restore_at_sunrise:
            if self._unsub_sunrise is not None:
                self._unsub_sunrise()
                self._unsub_sunrise = None
            next_sunrise = await self._get_next_sunrise()
            self._unsub_sunrise = async_track_point_in_time(
                self.hass, self._restore_trigger, next_sunrise
            )

        self.async_set_updated_data({"is_active": False})

    async def _dim_lights(self, start_brightness: int) -> None:
        target = max(1, int(self._min_brightness_pct / 100 * 255))
        interval = (self._dim_duration * 60) / DIM_STEPS
        for i in range(1, DIM_STEPS + 1):
            if not self._is_active:
                return
            brightness = int(start_brightness - (start_brightness - target) * i / DIM_STEPS)
            await self.hass.services.async_call("light", "turn_on", {
                "entity_id": self._lights,
                "rgb_color": RED_RGB,
                "brightness": max(1, brightness),
                "transition": interval,
            }, blocking=True)
            try:
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                return
