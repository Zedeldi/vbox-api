from vbox_api.api import VBoxAPI
from vbox_api.models import Machine


def test_base_interface_names(api: VBoxAPI) -> None:
    """Test names of base interface of API."""
    assert hasattr(api.interface.interface, "IVirtualBox")
    assert hasattr(api.interface.interface.IVirtualBox, "getMachines")


def test_pythonic_interface_names(api: VBoxAPI) -> None:
    """Test names of Pythonic interface of API."""
    assert hasattr(api.interface, "VirtualBox")
    assert hasattr(api.interface.VirtualBox, "get_machines")


def test_match_interface_name(api: VBoxAPI) -> None:
    """Test matching interface names by string."""
    assert api.interface.match_interface_name("get_machines") == "Machine"
    assert api.interface.match_interface_name("getMediums") == "Medium"


def test_get_interface_by_handle(api: VBoxAPI, random_machine: Machine) -> None:
    """Test getting interface name by handle returns correct string."""
    assert api.interface.get_interface_name_for_handle(api) == "VirtualBox"
    assert api.interface.get_interface_name_for_handle(random_machine) == "Machine"
