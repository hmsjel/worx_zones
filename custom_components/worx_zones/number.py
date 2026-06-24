from homeassistant.components.number import NumberEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    zones = coordinator.device.data["cfg"]["mz"]["s"]

    entities = []
    for z in zones:
        entities.append(ZoneDistance(coordinator, z["id"]))
        entities.append(ZoneProbability(coordinator, z["id"]))

    async_add_entities(entities)


class ZoneDistance(NumberEntity):
    def __init__(self, coordinator, zone_id):
        self.coordinator = coordinator
        self.zone_id = zone_id

    @property
    def name(self):
        return f"Zone {self.zone_id} Distance"

    @property
    def native_value(self):
        return self.coordinator.device.data["cfg"]["mz"]["s"][self.zone_id]["d"]

    async def async_set_native_value(self, value):
        self.coordinator.device.data["cfg"]["mz"]["s"][self.zone_id]["d"] = int(value)


class ZoneProbability(NumberEntity):
    def __init__(self, coordinator, zone_id):
        self.coordinator = coordinator
        self.zone_id = zone_id

    @property
    def name(self):
        return f"Zone {self.zone_id} Probability"

    @property
    def native_value(self):
        return self.coordinator.device.data["cfg"]["mz"]["s"][self.zone_id]["p"]

    async def async_set_native_value(self, value):
        self.coordinator.device.data["cfg"]["mz"]["s"][self.zone_id]["p"] = int(value)
