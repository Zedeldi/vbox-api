import pytest

from vbox_api.api import VBoxAPI
from vbox_api.models import Machine
from vbox_api.models.base import BaseModel


def test_machine_get_attribute(random_machine: Machine) -> None:
    """Test getting a property as an attribute."""
    assert random_machine.name == random_machine.get_name()


def test_base_model_register_handles(api: VBoxAPI) -> None:
    """Test getting multiple instances of model returns same object."""
    assert api.get_machines()[0] is api.get_machines()[0]


def test_model_register_classes(api: VBoxAPI) -> None:
    """Test creating a model class with the same name returns the same object."""
    assert BaseModel.from_name("Machine") is Machine


def test_get_model_from_attribute(random_machine: Machine) -> None:
    """Test getting an attribute returns a model."""
    assert isinstance(random_machine.audio_settings, BaseModel)
    assert isinstance(random_machine.get_audio_settings(), BaseModel)


def test_create_model_with_invalid_name_fails(api: VBoxAPI) -> None:
    """Test instantiating a model with an invalid name raises an exception."""
    model_cls = BaseModel.from_name("InvalidInterface")
    with pytest.raises(AttributeError):
        model_cls(api.ctx)


def test_model_as_handle(api: VBoxAPI, random_machine: Machine) -> None:
    """Test passing a model directly to interface as a handle."""
    assert api.interface.Machine.get_name(random_machine) == random_machine.name


def test_property_mixin(random_machine: Machine) -> None:
    """Test property mixin properties."""
    assert "name" in random_machine._getters
    assert random_machine._getters["name"]() == random_machine.name
