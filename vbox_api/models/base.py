import functools
from abc import ABC
from typing import Any, Optional, Type

from vbox_api.api.handle import Handle


class BaseModel(ABC):
    """Base class to handle model attributes and methods."""

    _models: dict[str, Type["BaseModel"]] = {}

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

    def get_property(self, name: str, use_model: bool = True) -> Any:
        """
        Return value of property at runtime.

        If use_model is True, return result as usable model if result is a
        valid handle.
        """
        result = self._properties[name](self.handle)
        if not use_model:
            return result
        interface_name = self.ctx.interface.match_interface_name(name)
        if interface_name:
            model = BaseModel.from_name(interface_name)
            if isinstance(result, list):
                return [self._get_model_from_value(model, value) for value in result]
            return self._get_model_from_value(model, result)
        return result

    def _get_model_from_value(self, model: Type["BaseModel"], value: Any) -> Any:
        """Return model if value is a handle else return value."""
        return (
            model(self.ctx, self.ctx.get_handle(value))
            if Handle.is_handle(value)
            else value
        )

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

    def to_dict(self, use_models: bool = True) -> dict:
        """
        Return dict to represent current state of model.

        If use_models is True, attempt to convert results to usable models.
        """
        info = {}
        for property_name in self._properties.keys():
            try:
                info[property_name] = self.get_property(property_name, use_models)
            except Exception:
                pass
        return info

    @classmethod
    def from_name(cls, model_name: str) -> Type["BaseModel"]:
        """Return subclass of BaseModel for model_name."""
        model = cls._models.get(model_name) or type(model_name, (cls,), {})
        cls.register_model(model)
        return model

    @classmethod
    def register_model(
        cls, model: Type["BaseModel"], name: Optional[str] = None
    ) -> Type["BaseModel"]:
        """
        Class method to register a model for the specified name.

        If name is not specified, use name of the model class.
        Can be used as a class decorator.
        """
        name = name or model.__name__
        cls._models[name] = model
        return model
