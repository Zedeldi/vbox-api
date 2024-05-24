from vbox_api.api import Context, Handle, VBoxAPI
from vbox_api.models import Machine, VirtualBox


def test_api_subclass(api: VBoxAPI) -> None:
    """Test API is subclass of VirtualBox model."""
    assert isinstance(api, VirtualBox)


def test_context_property(api: VBoxAPI) -> None:
    """Test context property of API."""
    assert isinstance(api.ctx, Context)
    assert api.ctx.api is api
    assert api.ctx.interface is api.interface


def test_get_handle_from_context(api: VBoxAPI) -> None:
    """Test getting handle from Context instance of API."""
    handle = api.ctx.get_handle(api.handle)
    assert isinstance(handle, Handle)
    assert isinstance(handle, str)
    assert handle == api.handle
    assert handle.ctx is api.ctx


def test_is_handle(api: VBoxAPI, random_string: str) -> None:
    """Test checking whether passed string is a handle."""
    assert Handle.is_handle(api.handle)
    assert not Handle.is_handle(random_string)


def test_get_machines(api: VBoxAPI) -> None:
    """Test getting machines from API."""
    machines = api.get_machines()
    assert all(isinstance(machine, Machine) for machine in machines)
