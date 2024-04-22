from types import TracebackType
from typing import Optional, Type

from vbox_api.api.handle import Handle
from vbox_api.models.base import BaseModel


class Session(BaseModel):
    """Context manager for a session."""

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
