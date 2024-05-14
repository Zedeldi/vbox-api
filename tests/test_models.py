def test_machine_get_attribute(random_machine: "Machine") -> None:
    """Test getting a property as an attribute."""
    assert random_machine.name == random_machine.get_name()


def test_base_model_register_handles(api: "VBoxAPI") -> None:
    """Test getting multiple instances of model returns same object."""
    assert api.get_machines()[0] is api.get_machines()[0]
