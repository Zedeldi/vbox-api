"""Object-oriented Python bindings to the VirtualBox SOAP API."""

from vbox_api.api import VBoxAPI
from vbox_api.interface import PythonicInterface, SOAPInterface

__all__ = ["PythonicInterface", "SOAPInterface", "VBoxAPI"]
