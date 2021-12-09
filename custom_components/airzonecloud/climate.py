import logging
from typing import List, Optional
from datetime import timedelta
from homeassistant.const import TEMP_CELSIUS, ATTR_TEMPERATURE
from homeassistant.util.temperature import convert as convert_temperature
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate import const as c_const
from homeassistant.components.climate.const import (
    HVAC_MODE_OFF,
    HVAC_MODE_HEAT,
    HVAC_MODE_COOL,
    HVAC_MODE_DRY,
    HVAC_MODE_FAN_ONLY,
    SUPPORT_TARGET_TEMPERATURE,
)
from .const import CONF_USERNAME, CONF_PASSWORD

# init logger
_LOGGER = logging.getLogger(__name__)

# default refresh interval
SCAN_INTERVAL = timedelta(seconds=10)

AIRZONECLOUD_ZONE_HVAC_MODES = [
    HVAC_MODE_OFF,
    HVAC_MODE_HEAT,
    HVAC_MODE_COOL,
    HVAC_MODE_DRY,
    HVAC_MODE_FAN_ONLY,
]


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Airzonecloud platform"""
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    if username is None or password is None:
        _LOGGER.error("missing username or password config")
        return

    from AirzoneCloud import AirzoneCloud

    api = None
    try:
        api = AirzoneCloud(username, password)
    except Exception as err:
        _LOGGER.error(err)
        hass.services.call(
            "persistent_notification",
            "create",
            {"title": "Airzonecloud error", "message": str(err)},
        )
        return

    entities = []
    for installation in api.installations:
        print(installation)
        for group in installation.groups:
            for device in group.devices:
                entities.append(AirzonecloudSystem(device))

    add_entities(entities)


class AirzonecloudZone(ClimateEntity):
    """Representation of an Airzonecloud Zone"""

    def __init__(self, azc_zone):
        """Initialize the zone"""
        self._azc_zone = azc_zone
        _LOGGER.info("init zone {} ({})".format(self.name, self.unique_id))

    @property
    def unique_id(self) -> Optional[str]:
        """Return a unique ID."""
        return "zone_" + self._azc_zone.id

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{} - {}".format(self._azc_zone.system.name, self._azc_zone.name)

    @property
    def temperature_unit(self):
        """Return the unit of measurement used by the platform."""
        return TEMP_CELSIUS

    @property
    def hvac_mode(self) -> str:
        """Return hvac operation ie. heat, cool mode."""
        mode = self._azc_zone.mode

        if self._azc_zone.is_on:
            if mode in ["air-cooling", "radiant-cooling", "combined-cooling"]:
                return HVAC_MODE_COOL

            if mode in ["air-heating", "radiant-heating", "combined-heating"]:
                return HVAC_MODE_HEAT

            if mode == "ventilation":
                return HVAC_MODE_FAN_ONLY

            if mode == "dehumidify":
                return HVAC_MODE_DRY

        return HVAC_MODE_OFF

    @property
    def hvac_modes(self) -> List[str]:
        """Return the list of available hvac operation modes."""
        return AIRZONECLOUD_ZONE_HVAC_MODES

    @property
    def current_humidity(self) -> Optional[float]:
        """Return the current humidity."""
        return self._azc_zone.current_humidity

    @property
    def current_temperature(self) -> Optional[float]:
        """Return the current temperature."""
        return self._azc_zone.current_temperature

    @property
    def target_temperature(self) -> Optional[float]:
        """Return the temperature we try to reach."""
        return self._azc_zone.target_temperature

    @property
    def target_temperature_step(self) -> Optional[float]:
        """Return the supported step of target temperature."""
        return 0.5

    def set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None:
            self._azc_zone.set_temperature(round(float(temperature), 1))

    def set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""
        if hvac_mode == HVAC_MODE_OFF:
            self.turn_off()
        else:
            if not self._azc_zone.is_on:
                self.turn_on()

            # set hvac mode on parent system
            if hvac_mode == HVAC_MODE_HEAT:
                self._azc_zone.system.set_mode("heating")
            elif hvac_mode == HVAC_MODE_COOL:
                self._azc_zone.system.set_mode("cooling")
            elif hvac_mode == HVAC_MODE_DRY:
                self._azc_zone.system.set_mode("dehumidify")
            elif hvac_mode == HVAC_MODE_FAN_ONLY:
                self._azc_zone.system.set_mode("ventilation")

    def turn_on(self):
        """Turn on."""
        self._azc_zone.turn_on()

    def turn_off(self):
        """Turn off."""
        self._azc_zone.turn_off()

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def min_temp(self) -> float:
        """Return the minimum temperature."""
        return convert_temperature(
            self._azc_zone.system.min_temp, TEMP_CELSIUS, self.temperature_unit
        )

    @property
    def max_temp(self) -> float:
        """Return the maximum temperature."""
        return convert_temperature(
            self._azc_zone.system.max_temp, TEMP_CELSIUS, self.temperature_unit
        )


class AirzonecloudSystem(ClimateEntity):
    """Representation of an Airzonecloud System"""

    hidden = True  # default hidden

    def __init__(self, azc_system):
        """Initialize the system"""
        self._azc_system = azc_system
        _LOGGER.info("init system {} ({})".format(self.name, self.unique_id))

    @property
    def unique_id(self) -> Optional[str]:
        """Return a unique ID."""
        return "system_" + self._azc_system.id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._azc_system.name

    @property
    def temperature_unit(self):
        """Return the unit of measurement used by the platform."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._azc_system.current_temperature

    @property
    def target_temperature(self):
        """Return the target temperature."""
        return self._azc_system.target_temperature


    @property
    def target_temperature_low(self):
        """Return the minimum target temperature."""
        return self._azc_system.min_temperature

    @property
    def target_temperature_high(self):
        """Return the maximum target temperature."""
        return self._azc_system.max_temperature

    @property
    def target_temperature_step(self):
        """Return the maximum target temperature step."""
        return 0.5

    @property
    def current_humidity(self):
        """Return the current humidity."""
        return self._azc_system.current_humidity

    @property
    def hvac_mode(self) -> str:
        """Return hvac operation ie. heat, cool mode."""
        mode = self._azc_system.mode

        if mode in ["cooling"]:
            return HVAC_MODE_COOL
        if mode in ["heating"]:
            return HVAC_MODE_HEAT
        if mode == "ventilation":
            return HVAC_MODE_FAN_ONLY
        if mode == "dehumidify":
            return HVAC_MODE_DRY
        return HVAC_MODE_OFF

    @property
    def hvac_modes(self) -> List[str]:
        """Return the list of available hvac operation modes."""
        hvac_modes = []
        for hvac_mode in self._azc_system.modes_availables:
            if hvac_mode == 'stop':
                hvac_modes.append(HVAC_MODE_OFF)
            if hvac_mode == 'heating':
                hvac_modes.append(HVAC_MODE_HEAT)
            elif hvac_mode == 'cooling':
                hvac_modes.append(HVAC_MODE_COOL)
            elif hvac_mode == 'dehumidify':
                hvac_modes.append(HVAC_MODE_DRY)
            elif hvac_mode == 'ventilation':
                hvac_modes.append(HVAC_MODE_FAN_ONLY)
        return hvac_modes

    def set_temperature(self, temperature: float) -> None:
        self._azc_system.set_temperature(temperature)

    def set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""
        if hvac_mode == HVAC_MODE_OFF:
            self._azc_system.set_mode("stop")
        if hvac_mode == HVAC_MODE_HEAT:
            self._azc_system.set_mode("heating")
        elif hvac_mode == HVAC_MODE_COOL:
            self._azc_system.set_mode("cooling")
        elif hvac_mode == HVAC_MODE_DRY:
            self._azc_system.set_mode("dehumidify")
        elif hvac_mode == HVAC_MODE_FAN_ONLY:
            self._azc_system.set_mode("ventilation")

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return c_const.SUPPORT_TARGET_TEMPERATURE

    def update(self):
        self._azc_system.refresh()
