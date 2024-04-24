from dataclasses import dataclass
from typing import Optional

from vbox_api.models.session import Session


@dataclass
class Context:
    """Dataclass to store context of operations."""

    api: "VBoxAPI"
    interface: "PythonicInterface"

    @property
    def api_handle(self) -> Optional["Handle"]:
        """Return handle of API instance."""
        return self.api.handle

    def get_session(self) -> Session:
        """Return Session object for Context instance."""
        return Session(self)
