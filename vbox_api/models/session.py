from types import TracebackType
from typing import Optional, Type

from vbox_api.api.handle import Handle
from vbox_api.models.base import BaseModel


class Session(BaseModel):
    """Context manager for a session."""

    def open(self, force: bool = False) -> None:
        """
        Open session by obtaining a handle.

        If force is True, open a new session even if already open.
        """
        if self.handle and not force:
            return None
        self.handle = Handle(
            self.ctx,
            self.ctx.interface.WebsessionManager.get_session_object(
                self.ctx.api_handle
            ),
        )

    def close(self) -> None:
        """Close session by releasing session handle and unlocking machine."""
        if not self.handle:
            return None
        if self.state == "Locked":
            self.unlock_machine()
        self.handle.release()
        self.handle = None

    def __enter__(self) -> Handle:
        self.open()
        return self.handle

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()
