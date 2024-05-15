from dataclasses import dataclass
from typing import Optional

from vbox_api.api.handle import Handle
from vbox_api.models.progress import Progress
from vbox_api.models.session import Session


@dataclass
class Context:
    """Dataclass to store context of operations."""

    api: "VBoxAPI"
    interface: "PythonicInterface"

    @property
    def api_handle(self) -> Optional[Handle]:
        """Return handle of API instance."""
        return self.api.handle

    def get_handle(self, handle: str) -> Handle:
        """Get Handle instance with current context and specified handle."""
        return Handle(self, handle)

    def get_session(self) -> Session:
        """Return Session object for Context instance."""
        return Session(self)

    def get_progress(self, handle: str) -> Progress:
        """Return Progress object for Context instance."""
        return Progress(self, self.get_handle(handle))
