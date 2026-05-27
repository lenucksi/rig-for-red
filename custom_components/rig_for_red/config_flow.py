import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

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
    DOMAIN,
    WEEKDAYS,
)


class RigForRedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            if not user_input[CONF_LIGHTS]:
                errors[CONF_LIGHTS] = "lights_required"

            if user_input.get(CONF_RESTORE_AT_SUNRISE) is False and not user_input.get(CONF_RESTORE_TIME):
                errors[CONF_RESTORE_TIME] = "restore_time_required"

            if not errors.get(CONF_LIGHTS):
                for entity_id in user_input[CONF_LIGHTS]:
                    if self.hass.states.get(entity_id) is None:
                        errors[CONF_LIGHTS] = "entity_not_found"
                        break

            if not errors:
                schedule_days = user_input[CONF_SCHEDULE_DAYS]
                schedule_time = user_input[CONF_SCHEDULE_TIME]
                schedule_days_joined = ",".join(schedule_days)
                title = f"Rig for Red ({schedule_time} [{schedule_days_joined}])"
                return self.async_create_entry(
                    title=title,
                    data=user_input,
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_LIGHTS): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="light",
                        multiple=True,
                    ),
                ),
                vol.Required(CONF_SCHEDULE_DAYS): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=WEEKDAYS,
                        multiple=True,
                        translation_key="weekdays",
                    ),
                ),
                vol.Required(CONF_SCHEDULE_TIME): selector.TimeSelector(),
                vol.Required(
                    CONF_DIM_DURATION_MINUTES,
                    default=DEFAULT_DIM_DURATION_MINUTES,
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=240,
                        mode="box",
                    ),
                ),
                vol.Required(
                    CONF_RESTORE_AT_SUNRISE,
                    default=DEFAULT_RESTORE_AT_SUNRISE,
                ): selector.BooleanSelector(),
                vol.Optional(CONF_RESTORE_TIME): selector.TimeSelector(),
                vol.Optional(
                    CONF_ADAPTIVE_LIGHTING_SWITCHES,
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="switch",
                        multiple=True,
                        integration="adaptive_lighting",
                    ),
                ),
                vol.Required(
                    CONF_MIN_BRIGHTNESS_PCT,
                    default=DEFAULT_MIN_BRIGHTNESS_PCT,
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=10,
                        mode="slider",
                    ),
                ),
                vol.Optional(
                    CONF_ENABLE_DEBUG_LOGGING,
                    default=DEFAULT_ENABLE_DEBUG_LOGGING,
                ): selector.BooleanSelector(),
            },
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_reconfigure(self, user_input=None):
        errors = {}
        entry = self._get_reconfigure_entry()

        if user_input is not None:
            if not user_input[CONF_LIGHTS]:
                errors[CONF_LIGHTS] = "lights_required"

            if user_input.get(CONF_RESTORE_AT_SUNRISE) is False and not user_input.get(CONF_RESTORE_TIME):
                errors[CONF_RESTORE_TIME] = "restore_time_required"

            if not errors.get(CONF_LIGHTS):
                for entity_id in user_input[CONF_LIGHTS]:
                    if self.hass.states.get(entity_id) is None:
                        errors[CONF_LIGHTS] = "entity_not_found"
                        break

            if not errors:
                self.hass.config_entries.async_update_entry(entry, data=user_input)
                return self.async_abort(reason="reconfigured")

        data = entry.data
        schema = {}
        schema[vol.Required(CONF_LIGHTS, default=data.get(CONF_LIGHTS, []))] = selector.EntitySelector(
            selector.EntitySelectorConfig(domain="light", multiple=True),
        )
        schema[vol.Required(CONF_SCHEDULE_DAYS, default=data.get(CONF_SCHEDULE_DAYS, []))] = selector.SelectSelector(
            selector.SelectSelectorConfig(options=WEEKDAYS, multiple=True, translation_key="weekdays"),
        )
        schema[vol.Required(CONF_SCHEDULE_TIME, default=data.get(CONF_SCHEDULE_TIME))] = selector.TimeSelector()
        schema[
            vol.Required(
                CONF_DIM_DURATION_MINUTES,
                default=data.get(CONF_DIM_DURATION_MINUTES, DEFAULT_DIM_DURATION_MINUTES),
            )
        ] = selector.NumberSelector(
            selector.NumberSelectorConfig(min=1, max=240, mode="box"),
        )
        schema[
            vol.Required(
                CONF_RESTORE_AT_SUNRISE,
                default=data.get(CONF_RESTORE_AT_SUNRISE, DEFAULT_RESTORE_AT_SUNRISE),
            )
        ] = selector.BooleanSelector()
        restore_time = data.get(CONF_RESTORE_TIME)
        if restore_time:
            schema[vol.Optional(CONF_RESTORE_TIME, default=restore_time)] = selector.TimeSelector()
        else:
            schema[vol.Optional(CONF_RESTORE_TIME)] = selector.TimeSelector()
        schema[
            vol.Optional(
                CONF_ADAPTIVE_LIGHTING_SWITCHES,
                default=data.get(CONF_ADAPTIVE_LIGHTING_SWITCHES, []),
            )
        ] = selector.EntitySelector(
            selector.EntitySelectorConfig(domain="switch", multiple=True, integration="adaptive_lighting"),
        )
        schema[
            vol.Required(
                CONF_MIN_BRIGHTNESS_PCT,
                default=data.get(CONF_MIN_BRIGHTNESS_PCT, DEFAULT_MIN_BRIGHTNESS_PCT),
            )
        ] = selector.NumberSelector(
            selector.NumberSelectorConfig(min=1, max=10, mode="slider"),
        )
        schema[
            vol.Optional(
                CONF_ENABLE_DEBUG_LOGGING,
                default=data.get(CONF_ENABLE_DEBUG_LOGGING, DEFAULT_ENABLE_DEBUG_LOGGING),
            )
        ] = selector.BooleanSelector()
        data_schema = vol.Schema(schema)

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=data_schema,
            errors=errors,
        )
