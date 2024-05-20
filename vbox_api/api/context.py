from dataclasses import dataclass
from typing import Optional

from vbox_api import api
from vbox_api.interface import PythonicInterface
from vbox_api.models import Progress, Session


@dataclass
class Context:
    """Dataclass to store context of operations."""

    api: "api.VBoxAPI"
    interface: PythonicInterface

    @property
    def api_handle(self) -> Optional["api.Handle"]:
        """Return handle of API instance."""
        return self.api.handle

    def get_handle(self, handle: str) -> "api.Handle":
        """Get Handle instance with current context and specified handle."""
        return api.Handle(self, handle)

    def get_session(self) -> Session:
        """Return Session object for Context instance."""
        return Session(self)

    def get_progress(self, handle: str) -> Progress:
        """Return Progress object for Context instance."""
        return Progress(self, self.get_handle(handle))
