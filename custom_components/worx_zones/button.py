from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ApplyZonesButton(coordinator)])


class ApplyZonesButton(ButtonEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def name(self):
        return "Apply Zones"

    async def async_press(self):
        cfg = self.coordinator.device.data["cfg"]

        total = sum(z["p"] for z in cfg["mz"]["s"])
        if total != 100:
            raise Exception(f"Total must be 100 (currently {total})")

        await self.coordinator.device.update_config(cfg)
