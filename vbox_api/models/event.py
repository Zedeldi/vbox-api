from threading import Thread
from typing import NoReturn

from vbox_api import api
from vbox_api.models.base import BaseModel, ModelRegister


class Event(BaseModel, metaclass=ModelRegister):
    """Class to handle Event attributes and methods."""

    def get_model(self) -> "Event":
        """Convert Event instance to object of class for type."""
        return self._get_model_from_value(
            self.handle, interface_name=self.type, base_model=Event
        )


class EventSource(BaseModel, metaclass=ModelRegister):
    """Class to handle EventSource attributes and methods."""


class EventListener(BaseModel, metaclass=ModelRegister):
    """Class to handle EventListener attributes and methods."""


class PassiveEventListener(EventListener):
    """Class to passively handle events, implicitly passing the EventSource."""

    def __init__(
        self, ctx: "api.Context", handle: "api.Handle", source: EventSource
    ) -> None:
        """Initialise base instance and add session attribute."""
        super().__init__(ctx, handle, model_name="EventListener")
        self.source = source

    def get_event(self, timeout_ms: int = -1) -> Event:
        """Return event from event source."""
        return self.source.get_event(self, timeout_ms)

    @classmethod
    def from_source(
        cls, source: EventSource, event_types: str | int = "Any"
    ) -> "PassiveEventListener":
        """Return instance of passive event listener from source."""
        listener = source.create_listener()
        source.register_listener(listener, event_types, False)
        return cls(source.ctx, listener.handle, source)

    @classmethod
    def from_ctx(
        cls, ctx: "api.Context", event_types: str | int = "Any"
    ) -> "PassiveEventListener":
        """Return instance of passive event listener from context."""
        source = ctx.api.get_event_source()
        return cls.from_source(source, event_types)


class EventListenerLoop(Thread):
    """Class to listen and handle events in a separate thread."""

    def __init__(self, listener: PassiveEventListener, daemon: bool = True) -> None:
        """Initialise event listener thread."""
        self.listener = listener
        super().__init__(target=self.event_loop, daemon=daemon)

    @staticmethod
    def handle_event(event) -> None:
        """Handle processing a passed event from event loop."""
        ...

    def event_loop(self) -> NoReturn:
        """Handle main event loop."""
        while True:
            event = self.listener.get_event(-1)
            self.handle_event(event)
