import asyncio

class WorxCoordinator:
    def __init__(self, hass, username, password):
        self.hass = hass
        self.username = username
        self.password = password
        self.device = None
        self.cloud = None

    async def async_setup(self):
        # ✅ IMPORT INSIDE THREAD (fixer blocking error)
        from pyworxcloud import WorxCloud

        for attempt in range(5):
            try:
                self.cloud = WorxCloud(
                    self.username,
                    self.password,
                    "worx"
                )

                await self.cloud.connect()

                # ✅ vent på devices
                for _ in range(10):
                    if self.cloud.devices:
                        break
                    await asyncio.sleep(1)

                if not self.cloud.devices:
                    raise Exception("No devices found")

                self.device = list(self.cloud.devices.values())[0]

                print("✅ Worx connected:", self.device.name)
                return

            except Exception as e:
                print(f"⚠️ Attempt {attempt+1} failed:", e)
                await asyncio.sleep(3)

        raise Exception("❌ Could not connect to Worx after retries")
