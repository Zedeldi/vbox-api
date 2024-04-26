import functools
from abc import ABC
from typing import Any, Optional, Type


class BaseModel(ABC):
    """Base class to handle model attributes and methods."""

    def __init__(self, ctx: "Context", handle: Optional["Handle"] = None) -> None:
        """Initialise instance of model with information."""
        self.ctx = ctx
        self._handle = handle
        interface = ctx.interface.get_interface(self.__class__.__name__)
        self._properties = interface.properties
        self._methods = interface.methods
        self.bind_methods()

    def __getattr__(self, name: str) -> Any:
        """Handle getting model attributes at runtime."""
        try:
            return self.get_property(name)
        except KeyError:
            raise AttributeError("Attribute not found.")

    def get_property(self, name: str) -> Any:
        """Return value of property at runtime."""
        value = self._properties[name](self.handle)
        interface_name = self.ctx.interface.match_interface_name(name)
        if interface_name:
            return BaseModel.from_name(interface_name)(
                self.ctx, self.ctx.get_handle(value)
            )
        return value

    def bind_methods(self) -> None:
        for method_name, method in self._methods.items():
            setattr(self, method_name, functools.partial(method, self.handle))

    @property
    def handle(self) -> Optional["Handle"]:
        """Return handle attribute."""
        return self._handle

    @handle.setter
    def handle(self, handle: Optional["Handle"]) -> None:
        """Set new handle and bind methods."""
        self._handle = handle
        self.bind_methods()

    def to_dict(self) -> dict:
        """Return dict to represent current state of model."""
        info = {}
        for property_name in self._properties.keys():
            try:
                info[property_name] = self.get_property(property_name)
            except Exception:
                pass
        return info

    @classmethod
    def from_name(cls, model_name: str) -> Type["BaseModel"]:
        """Return subclass of BaseModel for model_name."""
        return type(model_name, (cls,), {})
