from typing import Optional

from vbox_api.api.models import Machine
from vbox_api.api.session import Context, Handle, Session
from vbox_api.interface.base import BaseInterface, PythonicInterface


class VBoxAPI:
    """Class to handle API methods via an interface."""

    def __init__(self, interface: BaseInterface) -> None:
        """Initialise instance of API."""
        self.interface = PythonicInterface(interface)
        self.handle: Optional[Handle] = None
        self._session: Optional[Session] = None

    @property
    def ctx(self) -> Context:
        return Context(api=self, interface=self.interface, handle=self.handle)

    @property
    def session(self) -> Session:
        if not self._session:
            self._session = Session(self.ctx)
        return self._session

    def login(self, username: str, password: str, force: bool = False) -> bool:
        """
        Login with specified username and password.

        If force is specified, attempt authentication even if already logged in.
        """
        if self.handle and not force:
            raise RuntimeError("Already logged in.")
        self.handle = Handle(
            self.ctx, self.interface.WebsessionManager.logon(username, password)
        )
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
