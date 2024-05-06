import re
from abc import ABC
from typing import Optional

from vbox_api.mixins import PropertyMixin


class BaseInterface(ABC):
    """Define abstract base class for interface."""

    @staticmethod
    def get_matches(interface_name: str) -> set[str]:
        """Return case-folded set of strings to match interface name."""
        interface_name = (
            interface_name.casefold()
            .replace("_", "")
            .removeprefix("get")
            .removeprefix("set")
            .removeprefix("find")
            .removeprefix("i")
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

    def get_interface(self, interface_name: str) -> "ProxyInterface":
        """Get interface instance from interface_name."""
        return getattr(self, interface_name)


class ProxyInterface(PropertyMixin):
    """Class to represent a proxy interface."""


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
