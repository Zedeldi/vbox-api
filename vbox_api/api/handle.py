"""Module to provide methods for handle operations."""

import re

from vbox_api import api


class Handle(str):
    """Class to store and provide methods to release a handle."""

    HANDLE_REGEX = re.compile("[0-9a-fA-F]{16}-[0-9a-fA-F]{16}")

    def __new__(cls, ctx: "api.Context", handle: str) -> "Handle":
        """Return new string object."""
        obj = super().__new__(cls, handle)
        obj.ctx = ctx
        return obj

    def release(self) -> None:
        """Release managed object reference."""
        self.ctx.interface.ManagedObjectRef.release(self)

    @classmethod
    def is_handle(cls, handle: str) -> bool:
        """Return whether specified string matches handle format."""
        if not isinstance(handle, str):
            return False
        return bool(re.match(cls.HANDLE_REGEX, handle))
