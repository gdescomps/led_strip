"""Platform for light integration."""
from __future__ import annotations

import logging

import voluptuous as vol
from .set import Hub
from typing import Tuple

import homeassistant.util.color as color_util

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_HS_COLOR,
    PLATFORM_SCHEMA,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    LightEntity,
    COLOR_MODE_HS
)
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default='7777'): cv.string,
})

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the Led Strip platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config[CONF_HOST]
    port = config[CONF_PORT]

    # Setup connection with devices/cloud
    hub = Hub(host, port)

    # Verify that passed in configuration works
    # if not hub.is_valid_login():
    #     _LOGGER.error("Could not connect to AwesomeLight hub")
    #     return

    # Add devices
    # add_entities(AwesomeLight(light) for light in hub.lights())
    # add_entities(AwesomeLight(light) for light in hub)
    add_entities([LedStrip(hub)])


class LedStrip(LightEntity):
    """Representation of a LedStrip."""

    def __init__(self, light) -> None:
        """Initialize a LedStrip."""
        self._light = light
        # self._name = light.name
        self._name = light._host
        self._hs_color = [29.808,84.78]
        self._unique_id = light._host
        self._state = None
        self._brightness = 255

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def hs_color(self) -> tuple[float, float]:
        """Return the display name of this light."""
        return self._hs_color

    @property
    def unique_id(self) -> str:
        """Return the unique_id of this light."""
        return self._unique_id

    # @property
    # def supported_features(self) -> int:
    #     """Flag supported features."""
    #     flags = SUPPORT_FLASH
    #
    #     # All color modes except UNKNOWN,ON_OFF support transition
    #     modes = self._native_supported_color_modes
    #     if any(m not in (0, LightColorCapability.ON_OFF) for m in modes):
    #         flags |= SUPPORT_TRANSITION
    #     if self._static_info.effects:
    #         flags |= SUPPORT_EFFECT
    #     return flags

    @property
    def color_mode(self):
        return COLOR_MODE_HS

    @property
    def supported_color_modes(self) -> set[str] | None:
        """Flag supported color modes."""
        supported = set([COLOR_MODE_HS])
        return supported
        # return SUPPORT_LEDSTRIP

    @property
    def brightness(self):
        return self._brightness

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    # @property
    # def rgb_color(self) -> tuple[int, int, int] | None:
    #     """Return the rgb_color of the light."""
    #     return self._rgb_color

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on."""
        if ATTR_HS_COLOR in kwargs:
            self._hs_color = kwargs.get(ATTR_HS_COLOR)
            print("NEW hs_color : ", self._hs_color)
        elif ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
            print("NEW brightness: ", self._brightness)
        # else:
        #     print("No hs_color given")

        rgb_color = color_util.color_hsv_to_RGB(
            self._hs_color[0], self._hs_color[1], self._brightness / 255 * 100
        )

        # print("RGB: ", rgb_color)

        self._light.set_color(r=rgb_color[0], g=rgb_color[1], b=rgb_color[2])
        self._state = True

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        self._light.turn_off()
        self._state = False

    # def update(self) -> None:
    #     """Fetch new state data for this light.
    #
    #     This is the only method that should fetch new data for Home Assistant.
    #     """
    #     # self._light.update()
    #     self._state = self._light.is_on()
    #     self._brightness = self._light.brightness
