from typing import Literal

from vbox_api.api.handle import Handle
from vbox_api.models.base import BaseModel


class Machine(BaseModel):
    """Class to handle machine attributes and methods."""

    def start(self, front_end: Literal["gui", "headless", "sdl"] = "gui") -> None:
        """Start virtual machine with specified front_end."""
        with self.ctx.session as session_handle:
            self.launch_vm_process(session_handle, front_end)

    def lock(self, lock_type: Literal["Write", "Shared"] = "Shared") -> "Machine":
        """Lock machine and return mutable machine instance."""
        with self.ctx.session as session_handle:
            self.lock_machine(session_handle, lock_type)
            locked_machine = self.ctx.session.get_machine()
        return Machine(self.ctx, Handle(self.ctx, locked_machine))
