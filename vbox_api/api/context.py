from dataclasses import dataclass
from typing import Optional


@dataclass
class Context:
    """Dataclass to store context of operations."""

    api: "VBoxAPI"
    interface: "PythonicInterface"
    handle: Optional["Handle"]

    @property
    def session(self) -> "Session":
        """Return Session object from API of Context instance."""
        return self.api.session
