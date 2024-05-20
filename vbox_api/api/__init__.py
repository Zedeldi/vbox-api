"""General API classes to provide an entry point and store current state."""

from vbox_api.api.context import Context
from vbox_api.api.core import VBoxAPI
from vbox_api.api.handle import Handle

__all__ = ["Context", "Handle", "VBoxAPI"]
