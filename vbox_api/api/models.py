from abc import ABC
from typing import Type

from vbox_api.api.session import Context, Handle


class BaseModel(ABC):
    """Base class to handle model attributes and methods."""

    def __init__(self, ctx: Context, handle: Handle) -> None:
        """Initialise instance of model with information."""
        self.handle = handle
        interface = ctx.interface.get_interface(self.__class__.__name__)
        self._info = interface.get_info(self.handle)
        self._methods = interface.get_methods(self.handle)
        self.__dict__.update(self._info)
        self.__dict__.update(self._methods)

    @classmethod
    def from_name(cls, model_name: str) -> Type["BaseModel"]:
        """Return subclass of BaseModel for model_name."""
        return type(model_name, (cls,), {})


class Machine(BaseModel):
    """Class to handle machine attributes and methods."""
