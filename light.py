import requests

from homeassistant.components.light import (
    ATTR_BRIGHTNESS, Light, PLATFORM_SCHEMA, LightEntity)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
})
async def async_setup_entry(hass, config_entry, async_add_devices):
    name = config_entry.data['name']
    if name is None:
        name = config_entry.data['host']
    async_add_devices([DiyLight(name, config_entry.data['host'])])
    return True


class DiyLight(LightEntity):
    ip = ''

    def __init__(self, name, ip):
        """Initialize an AwesomeLight."""
        self.ip = ip
        self._name = name
        self._state = None
        self._brightness = None
        self.update()
    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light.
        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the light to turn on.
        You can skip the brightness part if your light does not support
        brightness control.
        """
        self._brightness = kwargs.get(ATTR_BRIGHTNESS, self._brightness if self._brightness is not None else 255)
        requests.get("http://"+self.ip+"/set?light=1&bri="+str(self._brightness))
        requests.get("http://"+self.ip+"/?on=true")

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        requests.get("http://"+self.ip+"/?on=false")

    def update(self):
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """
        data = requests.get("http://"+self.ip+"/get?light=1").json()
        self._state = data['on']
        self._brightness = data['bri']

    @property
    def supported_features(self):
        """Flag supported features."""
        return 1

