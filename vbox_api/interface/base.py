import re
from abc import ABC


class BaseInterface(ABC):
    """Define abstract base class for interface."""


class ProxyInterface:
    """Class to represent a proxy interface."""


class PythonicInterface:
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
        pattern = re.compile("((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")
        return pattern.sub(r"_\1", text).lower()
