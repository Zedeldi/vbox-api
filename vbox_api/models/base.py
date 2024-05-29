import functools
import types
from abc import ABC, ABCMeta
from collections import defaultdict
from typing import Any, Callable, Optional, Type
from weakref import WeakValueDictionary

from vbox_api import api
from vbox_api.mixins import PropertyMixin


class BaseModelRegister(ABCMeta, type):
    """Metaclass to register model instances on instantiation."""

    _handles: defaultdict[
        Type["BaseModel"], WeakValueDictionary["api.Handle", "BaseModel"]
    ] = defaultdict(WeakValueDictionary)

    def __call__(
        cls, ctx: "api.Context", handle: Optional["api.Handle"] = None, *args, **kwargs
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

    def __init__(
        self,
        ctx: "api.Context",
        handle: Optional["api.Handle"] = None,
        model_name: Optional[str] = None,
    ) -> None:
        """Initialise instance of model with information."""
        self.ctx = ctx
        self._handle = handle
        self._proxy_interface = self.ctx.interface.get_interface(
            model_name or self.__class__.__name__
        )
        self._bind_interface_methods()

    def __str__(self) -> str:
        """Return handle for string representation of instance if set."""
        return str(self.handle) if self.handle else repr(self)

    def __bool__(self) -> bool:
        """Return whether handle is valid."""
        return bool(self.handle)

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

    def _get_model_class_for_value(
        self, value: str, base_model: Optional[Type["BaseModel"]] = None
    ) -> Optional[Type["BaseModel"]]:
        """
        Return model class for value, else return None.

        If value is not a handle, try to match value to an interface name.
        """
        if not api.Handle.is_handle(value):
            match = self.ctx.interface.match_interface_name(value)
        else:
            match = self.ctx.interface.get_interface_name_for_handle(value)
        if not match:
            return None
        if not base_model:
            base_model = BaseModel
        return base_model.from_name(match)

    def _get_model_from_value(
        self,
        value: Any,
        interface_name: Optional[str] = None,
        base_model: Optional[Type["BaseModel"]] = None,
    ) -> Any:
        """
        Return model instance from value, or value if not a valid handle.

        If interface_name is specified, search by name instead of handle.
        """
        if not isinstance(value, str) or not api.Handle.is_handle(value):
            return value
        if interface_name:
            model = self._get_model_class_for_value(
                interface_name, base_model=base_model
            )
        else:
            model = self._get_model_class_for_value(value, base_model=base_model)
        if not model:
            return value
        return model(self.ctx, self.ctx.get_handle(value))

    def _parse_property(self, value: Any) -> Any:
        """Parse value of a property and return model instance if possible."""
        if not isinstance(value, list):
            return self._get_model_from_value(value)
        models = []
        for element in value:
            try:
                # Forcefully test if element is a mapping
                for key in element:
                    element[key] = self._get_model_from_value(element[key])
                models.append(element)
            except TypeError:
                models.append(self._get_model_from_value(element))
        return models

    def _wrap_property(self, func: Callable) -> Callable:
        """Wrap a property method to parse results."""

        @functools.wraps(func)
        def inner(*args, **kwargs) -> Any:
            return self._parse_property(func(*args, **kwargs))

        return inner

    def _bind_interface_methods(self) -> None:
        """Bind methods of interface to instance of model, passing handle."""
        for method_name, method in self._proxy_interface._methods.items():
            bound_method = functools.partial(method, self.handle)
            bound_method = functools.update_wrapper(bound_method, method)
            wrapped_method = self._wrap_property(bound_method)
            setattr(self, method_name, wrapped_method)

    @property
    def handle(self) -> Optional["api.Handle"]:
        """Return handle attribute."""
        return self._handle

    @handle.setter
    def handle(self, handle: Optional["api.Handle"]) -> None:
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
