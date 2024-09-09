import logging
import threading
from collections.abc import Callable
from dataclasses import dataclass
from pprint import pformat
from typing import Optional

from vbox_api import api
from vbox_api.constants import VBoxEventType
from vbox_api.models.base import BaseModel, ModelRegister

logger = logging.getLogger(__name__)


class Event(BaseModel, metaclass=ModelRegister):
    """Class to handle Event attributes and methods."""

    def get_model(self) -> "Event":
        """Convert Event instance to object of class for type."""
        return self._get_model_from_value(
            self.handle, interface_name=self.type, base_model=Event
        )


class EventSource(BaseModel, metaclass=ModelRegister):
    """Class to handle EventSource attributes and methods."""

    def __init__(self, *args, **kwargs) -> None:
        """Intialise parent class and add attributes for event source."""
        super().__init__(*args, **kwargs)
        self._debugger: Optional[EventSourceGroup] = None

    @property
    def debug(self) -> bool:
        """Return whether debugging is enabled."""
        return bool(self._debugger)

    @debug.setter
    def debug(self, state: bool) -> None:
        """Set debugging state via property."""
        if self._debugger:
            self._debugger.teardown()
            self._debugger = None
        else:
            listener = PassiveEventListener.from_source(self)
            loop = DebugEventListenerLoop(listener)
            loop.start()
            self._debugger = EventSourceGroup(source=self, listener=listener, loop=loop)


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

    def get_event(self, timeout_ms: int = -1) -> Optional[Event]:
        """Return event from event source."""
        return self.source.get_event(self, timeout_ms)

    def wait_for(self, event_types: list[VBoxEventType], **kwargs) -> Event:
        """
        Block until event of specified type is received, matching kwargs.

        All events will be consumed until event_type is found.
        Passed key-word arguments will be compared to attributes of the event
        model. If all of them match, it will be returned.
        """
        event = None
        while not event or event.type not in event_types:
            event = self.get_event(-1)
            if not event:
                continue
            for key, value in kwargs.items():
                try:
                    event_value = getattr(event.model, key)
                except AttributeError:
                    event = None
                    continue
                if event_value != value:
                    event = None
                    continue
        return event

    @classmethod
    def from_source(
        cls, source: EventSource, event_types: list[VBoxEventType] = [VBoxEventType.ANY]
    ) -> "PassiveEventListener":
        """Return instance of passive event listener from source."""
        listener = source.create_listener()
        source.register_listener(listener, event_types, False)
        return cls(source.ctx, listener.handle, source)

    @classmethod
    def from_ctx(
        cls, ctx: "api.Context", event_types: list[VBoxEventType] = [VBoxEventType.ANY]
    ) -> "PassiveEventListener":
        """Return instance of passive event listener from context."""
        source = ctx.api.get_event_source()
        return cls.from_source(source, event_types)


class EventListenerLoop(threading.Thread):
    """Class to listen and handle events in a separate thread."""

    def __init__(
        self,
        listener: PassiveEventListener,
        callback: Callable[[Event], None],
        daemon: bool = True,
    ) -> None:
        """Initialise event listener thread."""
        self.listener = listener
        self.callback = callback
        self.count = 0
        self._stop_event = threading.Event()
        super().__init__(target=self.loop, daemon=daemon)

    def _callback(self, event: Event) -> None:
        """Handle processing a passed event from event loop."""
        self.callback(event)
        self.count += 1

    def stop(self) -> None:
        """Set stop event to prevent additional events being processed."""
        self._stop_event.set()

    @property
    def stopped(self) -> bool:
        """Return whether stop event has been set."""
        return self._stop_event.is_set()

    def loop(self) -> None:
        """Handle main event loop."""
        while not self.stopped:
            event = self.listener.get_event(-1)
            if not event:
                continue
            self._callback(event)


class DebugEventListenerLoop(EventListenerLoop):
    """EventListenerLoop subclass to print all received events."""

    def __init__(self, listener: PassiveEventListener, *args, **kwargs) -> None:
        """Initialise parent event listener thread."""
        super().__init__(
            listener=listener, callback=self.display_event, *args, **kwargs
        )

    @staticmethod
    def display_event(event: Event) -> None:
        """Output event information to standard output."""
        data = {"event": event.to_dict(), "model": event.model.to_dict()}
        logger.debug(f"Received event of type '{event.type}':\n{pformat(data)}")


@dataclass
class EventSourceGroup:
    """Handle group of objects for an event source."""

    source: EventSource
    listener: EventListener
    loop: Optional[EventListenerLoop] = None

    def teardown(self) -> None:
        """Stop and unregister any grouped loops or listeners, respectively."""
        if self.loop:
            self.loop.stop()
        self.source.unregister_listener(self.listener)
