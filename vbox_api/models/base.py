import functools
from abc import ABC
from typing import Any, Optional, Type


class BaseModel(ABC):
    """Base class to handle model attributes and methods."""

    def __init__(self, ctx: "Context", handle: Optional["Handle"] = None) -> None:
        """Initialise instance of model with information."""
        self.ctx = ctx
        self.handle = handle
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
        return self._properties[name](self.handle)

    def bind_methods(self) -> None:
        for method_name, method in self._methods.items():
            setattr(self, method_name, functools.partial(method, self.handle))

    def to_dict(self) -> dict:
        """Return dict to represent current state of model."""
        info = {}
        for property_name, method in self._properties.items():
            try:
                info[property_name] = method(self.handle)
            except Exception:
                pass
        return info

    @classmethod
    def from_name(cls, model_name: str) -> Type["BaseModel"]:
        """Return subclass of BaseModel for model_name."""
        return type(model_name, (cls,), {})
