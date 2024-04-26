import re
from abc import ABC
from typing import Callable, Optional


class BaseInterface(ABC):
    """Define abstract base class for interface."""

    def match_interface_name(self, interface_name: str) -> Optional[str]:
        """Match an interface name, by returning best match or None."""
        interface_name = interface_name.casefold()
        for name in self.__dict__.keys():
            if name.casefold() in (interface_name, interface_name.replace("_", "")):
                return name
        return None

    def find_interface(self, interface_name: str) -> Optional["ProxyInterface"]:
        """Find an interface object by name, by returning best match or None."""
        matched_name = self.match_interface_name(interface_name)
        if not matched_name:
            return None
        return self.get_interface(matched_name)

    def get_interface(self, interface_name: str) -> "ProxyInterface":
        """Get interface instance from interface_name."""
        return getattr(self, interface_name)


class ProxyInterface:
    """Class to represent a proxy interface."""

    @property
    def methods(self) -> dict[str, Callable]:
        """Return list of all callable methods."""
        return {
            method_name: method
            for method_name, method in self.__dict__.items()
            if callable(method)
        }

    @property
    def properties(self) -> dict[str, Callable]:
        """Return dict of properties and associated get methods."""
        return {
            method_name.removeprefix("get").lstrip("_"): method
            for method_name, method in self.methods.items()
            if method_name.startswith("get")
        }


class PythonicInterface(BaseInterface):
    """Wrapper to convert methods to Python naming conventions."""

    def __init__(self, interface: BaseInterface, remove_prefix: bool = True) -> None:
        """
        Initialise wrapper interface instance.

        If remove_prefix is True, remove leading prefix from interface names.
        """
        self.interface = interface
        for interface_name, interface_obj in self.interface.__dict__.items():
            if not interface_name.startswith("I"):
                continue
            if remove_prefix:
                interface_name = interface_name.lstrip("I")
            proxy_interface = ProxyInterface()
            self.__setattr__(interface_name, proxy_interface)
            for method_name, method_callable in interface_obj.__dict__.items():
                method_name = self.camel_to_snake(method_name)
                proxy_interface.__setattr__(method_name, method_callable)

    @staticmethod
    def camel_to_snake(text: str) -> str:
        """Convert camelCase to snake_case."""
        pattern = re.compile("((DnD)|(?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")
        return pattern.sub(r"_\1", text).lower()
