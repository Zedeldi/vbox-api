from vbox_api.models.base import BaseModel, ModelRegister


class Unattended(BaseModel, metaclass=ModelRegister):
    """
    Class to handle unattended installer attributes and methods.

    Call VirtualBox.create_unattended_installer to create an Unattended object.
    """

    def configure(self) -> None:
        """Create required media and reconfigure virtual machine."""
        self.prepare()
        self.construct_media()
        self.reconfigure_vm()
