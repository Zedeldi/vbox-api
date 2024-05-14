import functools
import types
from abc import ABC, ABCMeta
from collections import defaultdict
from typing import Any, Callable, Optional, Type
from weakref import WeakValueDictionary

from vbox_api.api.handle import Handle
from vbox_api.mixins import PropertyMixin


class BaseModelRegister(ABCMeta, type):
    """Metaclass to register model instances on instantiation."""

    _handles: defaultdict[
        Type["BaseModel"], WeakValueDictionary["Handle", "BaseModel"]
    ] = defaultdict(WeakValueDictionary)

    def __call__(
        cls, ctx: "Context", handle: Optional["Handle"] = None, *args, **kwargs
    ) -> "BaseModel":
        """Return instance for given handle if exists, else create instance."""
        instance = cls._handles[cls].get(handle) if handle else None
        if instance is None:
            instance = super(BaseModelRegister, cls).__call__(
                ctx, handle, *args, **kwargs
            )
            if instance.handle:
                cls._handles[cls][instance.handle] = instance
        return instance


class ModelRegister(BaseModelRegister):
    """Metaclass for derived classes of BaseModel."""

    _models: dict[str, Type["BaseModel"]] = {}

    def __new__(
        cls, name: str, bases: tuple[Type["BaseModel"]], namespace: dict[str, Any]
    ) -> Type["BaseModel"]:
        """Return class for given name if exists, else create class."""
        model = cls._models.get(name)
        if model is None:
            model = super().__new__(cls, name, bases, namespace)
            cls._models[name] = model
        return model


class BaseModel(ABC, PropertyMixin, metaclass=BaseModelRegister):
    """Base class to handle model attributes and methods."""

    _PROPERTY_INTERFACE_ALIASES: dict[str, str] = {}
    _models: dict[str, Type["BaseModel"]] = {}

    def __init__(
        self,
        ctx: "Context",
        handle: Optional["Handle"] = None,
        model_name: Optional[str] = None,
    ) -> None:
        """Initialise instance of model with information."""
        self.ctx = ctx
        self._handle = handle
        self._proxy_interface = self.ctx.interface.get_interface(
            model_name or self.__class__.__name__
        )
        self._bind_interface_methods()

    def __getattr__(self, name: str) -> Any:
        """Handle getting model attributes at runtime."""
        try:
            return self._getters[name]()
        except KeyError:
            raise AttributeError(
                f"'{self.__class__.__name__}' model has no attribute '{name}'"
            ) from None

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
        self, interface_name: str, base_model: Optional[Type["BaseModel"]] = None
    ) -> Optional[Type["BaseModel"]]:
        """Return model class if match found, else return None."""
        interface_name = self._get_property_alias(interface_name) or interface_name
        match = self.ctx.interface.match_interface_name(interface_name)
        if not match:
            return None
        if not base_model:
            base_model = BaseModel
        return base_model.from_name(match)

    def _get_model_from_key_value(
        self, key: str, value: Any, base_model: Optional[Type["BaseModel"]] = None
    ) -> Any:
        """Return model from a key-value pair, or value if not a valid model."""
        model = self._get_model_for_interface(key, base_model=base_model)
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
        properties = (
            *self._proxy_interface._getters.values(),
            *self._proxy_interface._finders.values(),
            *self._proxy_interface._creators.values(),
        )
        for method_name, method in self._proxy_interface._methods.items():
            wrapped_method = functools.partial(method, self.handle)
            if method in properties:
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

    def from_dict(self, info: dict[str, Any]) -> None:
        """
        Set properties of model from passed dictionary.

        Attributes of submodels can be modified using nested dictionaries
        or by specifying a dot-separated path as the key.
        """
        for property_name, property_value in info.items():
            model = self
            property_path = property_name.split(".")
            for part in property_path[:-1]:
                model = model._getters[part]()
                property_path.pop(0)
            property_name = property_path.pop()  # Last remaining element
            if not isinstance(model, BaseModel):
                raise TypeError("Model must be an instance of 'BaseModel'")
            if isinstance(property_value, dict):
                model = model._getters[property_name]()
                model.from_dict(property_value)
            else:
                model._setters[property_name](property_value)

    @classmethod
    def from_name(cls, model_name: str) -> Type["BaseModel"]:
        """Return subclass of BaseModel for model_name."""
        return types.new_class(model_name, (cls,), {"metaclass": ModelRegister})
