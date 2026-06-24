import asyncio
from pyworxcloud import WorxCloud, exceptions


class WorxCoordinator:
    def __init__(self, hass, username, password):
        self.hass = hass
        self.username = username
        self.password = password
        self.device = None
        self.cloud = None

    async def async_setup(self):
        """Robust login + connect + device fetch"""

        for attempt in range(3):
            try:
                self.cloud = WorxCloud(
                    self.username,
                    self.password,
                    "worx"
                )

                # ✅ Korrekt flow (vigtigt)
                await self.cloud.connect()

                # ✅ VIGTIGT: giv API tid til at returnere devices
                for _ in range(10):
                    if self.cloud.devices:
                        break
                    await asyncio.sleep(1)

                if not self.cloud.devices:
                    raise Exception("No devices found from Worx API")

                self.device = list(self.cloud.devices.values())[0]

                print("✅ Worx connected:", self.device.name)
                return

            except exceptions.RequestError as e:
                print(f"⚠️ Worx login attempt {attempt+1} failed:", e)
                await asyncio.sleep(3)

        raise Exception("❌ Could not connect to Worx after retries")
