from homeassistant.config_entries import ConfigEntry


class MockConfigEntry(ConfigEntry):
    def __init__(self, *, domain, data, entry_id=None, **kwargs):
        super().__init__(
            version=kwargs.pop("version", 1),
            minor_version=kwargs.pop("minor_version", 1),
            domain=domain,
            title=kwargs.pop("title", ""),
            source=kwargs.pop("source", "user"),
            data=data.copy(),
            options=kwargs.pop("options", {}),
            unique_id=kwargs.pop("unique_id", None),
            discovery_keys=kwargs.pop("discovery_keys", {}),
            subentries_data=kwargs.pop("subentries_data", None),
            pref_disable_new_entities=kwargs.pop("pref_disable_new_entities", False),
            pref_disable_polling=kwargs.pop("pref_disable_polling", False),
        )
        if entry_id is not None:
            object.__setattr__(self, "entry_id", entry_id)

    def add_to_hass(self, hass):
        self._hass = hass
        hass.config_entries._entries[self.entry_id] = self
