from homeassistant import config_entries
from homeassistant.helpers import selector
import voluptuous as vol

from .const import (
    DOMAIN,
    CONF_LIGHTS,
    CONF_SCHEDULE_DAYS,
    CONF_SCHEDULE_TIME,
    CONF_DIM_DURATION_MINUTES,
    CONF_RESTORE_AT_SUNRISE,
    CONF_RESTORE_TIME,
    CONF_ADAPTIVE_LIGHTING_SWITCHES,
    CONF_MIN_BRIGHTNESS_PCT,
    DEFAULT_DIM_DURATION_MINUTES,
    DEFAULT_MIN_BRIGHTNESS_PCT,
    DEFAULT_RESTORE_AT_SUNRISE,
    WEEKDAYS,
)


class RigForRedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            if not user_input[CONF_LIGHTS]:
                errors[CONF_LIGHTS] = "lights_required"

            if (
                user_input.get(CONF_RESTORE_AT_SUNRISE) is False
                and not user_input.get(CONF_RESTORE_TIME)
            ):
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
                title = (
                    f"Rig for Red ({schedule_time} [{schedule_days_joined}])"
                )
                return self.async_create_entry(
                    title=title, data=user_input
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_LIGHTS): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="light", multiple=True
                    )
                ),
                vol.Required(CONF_SCHEDULE_DAYS): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=WEEKDAYS,
                        multiple=True,
                        translation_key="weekdays",
                    )
                ),
                vol.Required(CONF_SCHEDULE_TIME): selector.TimeSelector(),
                vol.Required(
                    CONF_DIM_DURATION_MINUTES,
                    default=DEFAULT_DIM_DURATION_MINUTES,
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1, max=240, mode="box"
                    )
                ),
                vol.Required(
                    CONF_RESTORE_AT_SUNRISE,
                    default=DEFAULT_RESTORE_AT_SUNRISE,
                ): selector.BooleanSelector(),
                vol.Optional(CONF_RESTORE_TIME): selector.TimeSelector(),
                vol.Optional(
                    CONF_ADAPTIVE_LIGHTING_SWITCHES
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="switch",
                        multiple=True,
                        integration="adaptive_lighting",
                    )
                ),
                vol.Required(
                    CONF_MIN_BRIGHTNESS_PCT,
                    default=DEFAULT_MIN_BRIGHTNESS_PCT,
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1, max=10, mode="slider"
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
