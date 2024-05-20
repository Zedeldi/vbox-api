from typing import Optional

from vbox_api import api
from vbox_api.interface.base import BaseInterface, PythonicInterface
from vbox_api.models.virtualbox import VirtualBox


class VBoxAPI(VirtualBox):
    """Class to handle API methods via a VirtualBox interface."""

    def __init__(
        self, interface: BaseInterface, handle: Optional["api.Handle"] = None
    ) -> None:
        """Initialise instance of API."""
        if not isinstance(interface, PythonicInterface):
            interface = PythonicInterface(interface)
        self.interface = interface
        super().__init__(self.get_context(), handle, model_name="VirtualBox")

    def get_context(self) -> "api.Context":
        """Return instance of current Context for API."""
        return api.Context(api=self, interface=self.interface)
