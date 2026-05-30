DOMAIN = "rig_for_red"
VERSION = "0.3.3"  # x-release-please-version

CONF_LIGHTS = "lights"
CONF_SCHEDULE_DAYS = "schedule_days"
CONF_SCHEDULE_TIME = "schedule_time"
CONF_DIM_DURATION_MINUTES = "dim_duration_minutes"
CONF_RESTORE_AT_SUNRISE = "restore_at_sunrise"
CONF_RESTORE_TIME = "restore_time"
CONF_ADAPTIVE_LIGHTING_SWITCHES = "adaptive_lighting_switches"
CONF_MIN_BRIGHTNESS_PCT = "min_brightness_pct"
CONF_ENABLE_DEBUG_LOGGING = "enable_debug_logging"
CONF_AL_SLEEP_MODE = "al_sleep_mode"
CONF_RGB_PRESET = "rgb_preset"
CONF_RGB_CUSTOM = "rgb_custom"

DEFAULT_DIM_DURATION_MINUTES = 60
DEFAULT_MIN_BRIGHTNESS_PCT = 5
DEFAULT_ENABLE_DEBUG_LOGGING = False
DEFAULT_AL_SLEEP_MODE = False
DEFAULT_RGB_PRESET = "red"
DEFAULT_RGB_CUSTOM = [255, 0, 0]
DEFAULT_RESTORE_AT_SUNRISE = True

DIM_STEPS = 10
RED_RGB = [255, 0, 0]
BLUE_RGB = [0, 64, 255]
WHITE_COLOR_TEMP_KELVIN = 2700

WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
