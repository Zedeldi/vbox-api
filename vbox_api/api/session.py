from dataclasses import dataclass
from types import TracebackType
from typing import Optional, Type

from vbox_api.interface.base import PythonicInterface


@dataclass
class Context:
    """Dataclass to store context of operations."""

    api: "VBoxAPI"
    interface: PythonicInterface
    handle: Optional["Handle"]

    @property
    def session(self) -> "Session":
        """Return Session object from Context instance."""
        return Session(self)


class Handle(str):
    """Class to store and provide methods to release a handle."""

    def __new__(cls, ctx: Context, handle: str) -> "Handle":
        """Return new string object."""
        obj = super().__new__(cls, handle)
        obj.ctx = ctx
        return obj

    def release(self) -> None:
        """Release managed object reference."""
        self.ctx.interface.ManagedObjectRef.release(self)


class Session:
    """Context manager for a session."""

    def __init__(self, ctx: Context) -> None:
        """Initialise instance of session object with valid handle."""
        self.ctx = ctx
        self.handle: Optional[Handle] = None

    def open(self) -> None:
        """Open session by obtaining a handle."""
        self.handle = Handle(
            self.ctx,
            self.ctx.interface.WebsessionManager.get_session_object(self.ctx.handle),
        )

    def close(self) -> None:
        """Close session by releasing session handle."""
        self.handle.release()
        self.handle = None

    def __enter__(self) -> Handle:
        if not self.handle:
            self.open()
        return self.handle

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()
