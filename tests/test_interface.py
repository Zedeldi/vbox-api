def test_base_interface_names(api: "VBoxAPI") -> None:
    """Test names of base interface of API."""
    assert hasattr(api.interface.interface, "IVirtualBox")


def test_pythonic_interface_names(api: "VBoxAPI") -> None:
    """Test names of Pythonic interface of API."""
    assert hasattr(api.interface, "VirtualBox")
