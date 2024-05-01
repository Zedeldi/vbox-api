import functools
from typing import Callable, Iterable, Optional

from vbox_api.api.context import Context
from vbox_api.api.handle import Handle
from vbox_api.interface.base import BaseInterface, PythonicInterface
from vbox_api.models.base import BaseModel
from vbox_api.models.machine import Machine


def register_handles(func: Callable) -> Callable:
    """Register handles to models to API instance."""

    @functools.wraps(func)
    def inner(self, *args, **kwargs) -> Optional[Iterable[BaseModel] | BaseModel]:
        result = func(self, *args, **kwargs)
        if not result:
            return result
        if isinstance(result, Iterable):
            for model in result:
                self._handles[model.handle] = model
        else:
            self._handles[result.handle] = result
        return result

    return inner


class VBoxAPI:
    """Class to handle API methods via a VirtualBox interface."""

    def __init__(self, interface: BaseInterface) -> None:
        """Initialise instance of API."""
        self.interface = PythonicInterface(interface)
        self.virtualbox = BaseModel.from_name("VirtualBox")(self.ctx)
        self._handles: dict[str, BaseModel] = {}

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

    def logoff(self) -> None:
        """Logoff current session."""
        self.interface.WebsessionManager.logoff(self.virtualbox.handle)
        self.virtualbox.handle = None

    @property
    @register_handles
    def machines(self) -> list[Machine]:
        """Return list of Machine instances."""
        return [
            self._handles.get(machine.handle, machine)
            for machine in self.virtualbox.get_machines()
        ]

    @register_handles
    def find_machine(self, name_or_id: str) -> Optional[Machine]:
        """Return machine matching specified name or ID."""
        try:
            machine = self.virtualbox.find_machine(name_or_id)
        except Exception:
            return None
        return self._handles.get(machine.handle, machine)
