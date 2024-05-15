from vbox_api.models.base import BaseModel, ModelRegister


class VirtualBox(BaseModel, metaclass=ModelRegister):
    """
    Class to handle VirtualBox attributes and methods.

    This model is the main entry-point of the API.
    """

    _PROPERTY_INTERFACE_ALIASES: dict[str, str] = {
        "DVDImages": "IMedium",
        "HardDisks": "IMedium",
    }

    def login(self, username: str, password: str, force: bool = False) -> bool:
        """
        Login with specified username and password.

        If force is specified, attempt authentication even if already logged in.
        """
        if self.handle and not force:
            raise RuntimeError("Already logged in and force not specified")
        try:
            self.handle = self.ctx.get_handle(
                self.ctx.interface.WebsessionManager.logon(username, password)
            )
            return True
        except Exception:
            return False

    def logoff(self) -> None:
        """Logoff current session."""
        self.ctx.interface.WebsessionManager.logoff(self.handle)
        self.handle = None

    def create_machine_with_defaults(
        self,
        name: str,
        groups: str = "/",
        os_type_id: str = "Other_64",
        register_machine: bool = True,
    ) -> "Machine":
        """Create machine with specified name and default settings for OS type."""
        machine = self.create_machine("", name, groups, os_type_id, "", "", "", "")
        machine.apply_defaults("")
        if register_machine:
            self.register_machine(machine)
        return machine
