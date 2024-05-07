def test_machine_get_attribute(random_machine: "Machine") -> None:
    """Test getting a property as an attribute."""
    assert random_machine.name == random_machine.get_name()
