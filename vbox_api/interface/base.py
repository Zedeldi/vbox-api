"""Base interface classes to be used by an interface implementation."""

import re
from abc import ABC
from typing import Callable, Optional

from vbox_api.mixins import PropertyMixin


class BaseInterface(ABC):
    """Define abstract base class for interface."""

    def _register_interface(
        self, interface_name: str, proxy_interface: "ProxyInterface"
    ) -> None:
        """Register proxy interface to interface instance."""
        if not isinstance(proxy_interface, ProxyInterface):
            raise TypeError(
                "Passed interface object is not an instance of 'ProxyInterface'"
            )
        setattr(self, interface_name, proxy_interface)

    @staticmethod
    def get_matches(interface_name: str) -> set[str]:
        """Return case-folded set of strings to match interface name."""
        interface_name = (
            interface_name.casefold()
            .replace("_", "")
            .removeprefix("get")
            .removeprefix("set")
            .removeprefix("find")
            .removeprefix("current")
            .removeprefix("create")
            .removeprefix("i")
            .removeprefix("on")
            .removesuffix("byid")
            .removesuffix("byname")
            .removesuffix("bygroups")
        )
        matches = {
            interface_name,
            interface_name.removesuffix("s"),
            interface_name.removesuffix("es"),
        }
        matches.update([f"i{match}" for match in matches])
        matches.update([f"{match}event" for match in matches])
        return matches

    def match_interface_name(self, interface_name: str) -> Optional[str]:
        """Match an interface name, by returning best match or None."""
        matches = self.get_matches(interface_name)
        for name in self.__dict__.keys():
            if name.casefold() in matches:
                return name
        return None

    def find_interface(self, interface_name: str) -> Optional["ProxyInterface"]:
        """Find an interface object by name, by returning best match or None."""
        matched_name = self.match_interface_name(interface_name)
        if not matched_name:
            return None
        return self.get_interface(matched_name)

    def get_interface_name_for_handle(self, handle: str) -> Optional[str]:
        """Return interface name for specified handle."""
        return self.IManagedObjectRef.getInterfaceName(handle)

    def get_interface_for_handle(self, handle: str) -> Optional["ProxyInterface"]:
        """Return interface object for specified handle or None."""
        interface_name = self.get_interface_name_for_handle(handle)
        if not interface_name:
            return None
        return self.get_interface(interface_name)

    def get_interface(self, interface_name: str) -> "ProxyInterface":
        """Get interface instance from interface_name."""
        return getattr(self, interface_name)


class ProxyInterface(PropertyMixin):
    """Class to represent a proxy interface."""

    def _register_method(self, method_name: str, method: Callable) -> None:
        """Register method to proxy interface instance."""
        if not callable(method):
            raise TypeError("Passed method is not callable")
        setattr(self, method_name, method)


class PythonicInterface(BaseInterface):
    """Wrapper to convert methods to Python naming conventions."""

    def __init__(self, interface: BaseInterface, remove_prefix: bool = True) -> None:
        """
        Initialise wrapper interface instance.

        If remove_prefix is True, remove leading prefix from interface names.
        """
        self.interface = interface
        self._remove_prefix = remove_prefix
        for interface_name, interface_obj in self.interface.__dict__.items():
            if not interface_name.startswith("I"):
                continue
            if self._remove_prefix:
                interface_name = interface_name.removeprefix("I")
            proxy_interface = ProxyInterface()
            self._register_interface(interface_name, proxy_interface)
            for method_name, method_callable in interface_obj.__dict__.items():
                method_name = self.camel_to_snake(method_name)
                proxy_interface._register_method(method_name, method_callable)

    def get_interface_name_for_handle(self, handle: str) -> Optional[str]:
        """Return interface name for specified handle."""
        if self._remove_prefix:
            interface_name = self.ManagedObjectRef.get_interface_name(handle)
            if not interface_name:
                return None
            return interface_name.removeprefix("I")
        return self.IManagedObjectRef.get_interface_name(handle)

    @staticmethod
    def camel_to_snake(text: str) -> str:
        """Convert camelCase to snake_case."""
        pattern = re.compile("((DnD)|(?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")
        return pattern.sub(r"_\1", text).lower()
