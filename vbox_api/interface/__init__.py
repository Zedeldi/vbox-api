"""Interface classes to communicate with the VirtualBox API."""

from vbox_api.interface.base import PythonicInterface
from vbox_api.interface.soap import SOAPInterface

__all__ = ["PythonicInterface", "SOAPInterface"]
