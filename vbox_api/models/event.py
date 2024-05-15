from vbox_api.models.base import BaseModel, ModelRegister


class Event(BaseModel, metaclass=ModelRegister):
    """Class to handle Event attributes and methods."""

    _PROPERTY_INTERFACE_ALIASES: dict[str, str] = {
        "Listener": "IEventListener",
        "Source": "IEventSource",
    }

    def get_model(self) -> "Event":
        """Convert Event instance to object of class for type."""
        return self._get_model_from_key_value(self.type, self.handle, base_model=Event)


class EventSource(BaseModel, metaclass=ModelRegister):
    """Class to handle EventSource attributes and methods."""

    _PROPERTY_INTERFACE_ALIASES: dict[str, str] = {"Listener": "IEventListener"}


class EventListener(BaseModel, metaclass=ModelRegister):
    """Class to handle EventListener attributes and methods."""
