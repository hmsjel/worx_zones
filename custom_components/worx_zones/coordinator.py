from pyworxcloud import WorxCloud

class WorxCoordinator:
    def __init__(self, hass, username, password):
        self.hass = hass
        self.username = username
        self.password = password
        self.device = None

    async def async_setup(self):
        self.cloud = WorxCloud(self.username, self.password, "worx")
        await self.cloud.authenticate()
        await self.cloud.connect()

        self.device = list(self.cloud.devices.values())[0]
