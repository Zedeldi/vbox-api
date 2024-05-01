import functools
from abc import ABC
from typing import Any, Callable, Optional, Type

from vbox_api.api.handle import Handle
from vbox_api.mixins import PropertyMixin


class BaseModel(ABC, PropertyMixin):
    """Base class to handle model attributes and methods."""

    _PROPERTY_INTERFACE_ALIASES: dict[str, str] = {}
    _models: dict[str, Type["BaseModel"]] = {}

    def __init__(self, ctx: "Context", handle: Optional["Handle"] = None) -> None:
        """Initialise instance of model with information."""
        self.ctx = ctx
        self._handle = handle
        self.interface = self.ctx.interface.get_interface(self.__class__.__name__)
        self._bind_interface_methods()

    def __getattr__(self, name: str) -> Any:
        """Handle getting model attributes at runtime."""
        try:
            return self._getters[name]()
        except KeyError:
            raise AttributeError("Attribute not found.")

    def __setattr__(self, name: str, value: Any) -> None:
        """Handle setting model attributes at runtime."""
        try:
            self._setters[name](value)
        except KeyError:
            super().__setattr__(name, value)

    def _get_property_alias(self, interface_name: str) -> Optional[str]:
        """Return alias of interface_name, if any."""
        matches = self.ctx.interface.get_matches(interface_name)
        for key, value in self._PROPERTY_INTERFACE_ALIASES.items():
            if key.casefold() in matches:
                return value
        return None

    def _get_model_for_interface(
        self, interface_name: str
    ) -> Optional[Type["BaseModel"]]:
        """Return model class if match found, else return None."""
        interface_name = self._get_property_alias(interface_name) or interface_name
        match = self.ctx.interface.match_interface_name(interface_name)
        if not match:
            return None
        return BaseModel.from_name(match)

    def _get_model_from_key_value(self, key: str, value: Any) -> Any:
        """Return model from a key-value pair, or value if not a valid model."""
        model = self._get_model_for_interface(key)
        if not model or not Handle.is_handle(value):
            return value
        return model(self.ctx, self.ctx.get_handle(value))

    def _parse_property(self, name: str, value: Any) -> Any:
        """Parse value of a property and return model instance if possible."""
        if not isinstance(value, list):
            return self._get_model_from_key_value(name, value)
        models = []
        for element in value:
            try:
                # Forcefully test if element is a mapping
                for key in element:
                    element[key] = self._get_model_from_key_value(key, element[key])
                models.append(element)
            except TypeError:
                models.append(self._get_model_from_key_value(name, element))
        return models

    def _wrap_property(self, name: str, func: Callable) -> Callable:
        """Wrap a property method to parse results."""

        def inner(*args, **kwargs) -> Any:
            return self._parse_property(name, func(*args, **kwargs))

        return inner

    def _bind_interface_methods(self) -> None:
        """Bind methods of interface to instance of model, passing handle."""
        for method_name, method in self.interface._methods.items():
            wrapped_method = functools.partial(method, self.handle)
            if (
                method in self.interface._getters.values()
                or method in self.interface._finders.values()
            ):
                wrapped_method = self._wrap_property(method_name, wrapped_method)
            setattr(self, method_name, wrapped_method)

    @property
    def handle(self) -> Optional["Handle"]:
        """Return handle attribute."""
        return self._handle

    @handle.setter
    def handle(self, handle: Optional["Handle"]) -> None:
        """Set new handle and bind methods."""
        self._handle = handle
        self._bind_interface_methods()

    def to_dict(self) -> dict:
        """Return dict to represent current state of model."""
        info = {}
        for property_name, method in self._getters.items():
            try:
                info[property_name] = method()
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
