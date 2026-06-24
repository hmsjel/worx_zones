from .const import DOMAIN

async def async_setup(hass, config):
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass, entry):
    from .coordinator import WorxCoordinator

    coordinator = WorxCoordinator(
        hass,
        entry.data["username"],
        entry.data["password"],
    )

    await coordinator.async_setup()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        ["number", "button"]
    )

    return True
