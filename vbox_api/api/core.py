from typing import Optional

from vbox_api.api.context import Context
from vbox_api.api.handle import Handle
from vbox_api.interface.base import BaseInterface, PythonicInterface
from vbox_api.models.machine import Machine
from vbox_api.models.session import Session


class VBoxAPI:
    """Class to handle API methods via an interface."""

    def __init__(self, interface: BaseInterface) -> None:
        """Initialise instance of API."""
        self.interface = PythonicInterface(interface)
        self.handle: Optional[Handle] = None

    @property
    def ctx(self) -> Context:
        return Context(api=self, interface=self.interface)

    def login(self, username: str, password: str, force: bool = False) -> bool:
        """
        Login with specified username and password.

        If force is specified, attempt authentication even if already logged in.
        """
        if self.handle and not force:
            raise RuntimeError("Already logged in.")
        try:
            self.handle = Handle(
                self.ctx, self.interface.WebsessionManager.logon(username, password)
            )
            return True
        except Exception:
            return False

    @property
    def machines(self) -> list[Machine]:
        """Return list of Machine instances."""
        return [
            Machine(self.ctx, Handle(self.ctx, handle))
            for handle in self.interface.VirtualBox.get_machines(self.handle)
        ]
