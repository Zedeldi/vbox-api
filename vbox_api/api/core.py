from typing import Optional

from vbox_api.api.context import Context
from vbox_api.api.handle import Handle
from vbox_api.interface.base import BaseInterface, PythonicInterface
from vbox_api.models.base import BaseModel
from vbox_api.models.machine import Machine


class VBoxAPI:
    """Class to handle API methods via a VirtualBox interface."""

    def __init__(self, interface: BaseInterface) -> None:
        """Initialise instance of API."""
        self.interface = PythonicInterface(interface)
        self.virtualbox = BaseModel.from_name("VirtualBox")(self.ctx)

    @property
    def handle(self) -> Optional[Handle]:
        """Return handle of VirtualBox instance."""
        return self.virtualbox.handle

    @property
    def ctx(self) -> Context:
        return Context(api=self, interface=self.interface)

    def login(self, username: str, password: str, force: bool = False) -> bool:
        """
        Login with specified username and password.

        If force is specified, attempt authentication even if already logged in.
        """
        if self.virtualbox.handle and not force:
            raise RuntimeError("Already logged in.")
        try:
            self.virtualbox.handle = self.ctx.get_handle(
                self.interface.WebsessionManager.logon(username, password)
            )
            return True
        except Exception:
            return False

    @property
    def machines(self) -> list[Machine]:
        """Return list of Machine instances."""
        return [
            Machine(self.ctx, self.ctx.get_handle(handle))
            for handle in self.virtualbox.get_machines()
        ]
