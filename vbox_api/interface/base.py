import functools
import re
from abc import ABC


class BaseInterface(ABC):
    """Define abstract base class for interface."""

    def get_interface(self, interface_name: str) -> "ProxyInterface":
        """Get interface instance from interface_name."""
        return getattr(self, interface_name)


class ProxyInterface:
    """Class to represent a proxy interface."""

    def get_methods(self, handle: str) -> dict:
        """Get dict of methods bound to handle."""
        d = {}
        for method_name, method in self.__dict__.items():
            if not callable(method):
                continue
            d[method_name] = functools.partial(method, handle)
        return d

    def get_info(self, handle: str) -> dict:
        """Get dict of information for handle from interface."""
        d = {}
        for method_name, method in self.__dict__.items():
            if not method_name.startswith("get"):
                continue
            try:
                d[method_name.removeprefix("get").lstrip("_")] = method(handle)
            except Exception:
                pass
        return d


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
        pattern = re.compile("((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")
        return pattern.sub(r"_\1", text).lower()
