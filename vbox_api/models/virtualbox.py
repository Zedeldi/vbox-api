from pathlib import Path
from typing import Optional

from vbox_api.models.base import BaseModel, ModelRegister
from vbox_api.models.machine import Machine
from vbox_api.models.medium import Medium


class VirtualBox(BaseModel, metaclass=ModelRegister):
    """
    Class to handle VirtualBox attributes and methods.

    This model is the main entry-point of the API.
    """

    _PROPERTY_INTERFACE_ALIASES: dict[str, str] = {
        "DVDImages": "IMedium",
        "HardDisks": "IMedium",
        "FloppyImages": "IMedium",
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

    def find_model(self, model_name: str, name_or_id: str) -> Optional[BaseModel]:
        """Call appropriate method to find model_name from name_or_id."""
        model_name = model_name.replace("_", "")
        for method_name, method in self._methods.items():
            method_name = (
                method_name.split("_by_")[0].replace("_", "").removeprefix("find")
            )
            if method_name.casefold() == model_name.casefold():
                break
        else:
            raise ValueError(
                f"Model name '{model_name}' has no finder method"
            ) from None
        try:
            return method(name_or_id)
        except Exception:
            return None

    def get_guest_os_type_ids(self) -> set[str]:
        """Return set of guest OS type IDs."""
        return {os_type.id for os_type in self.guest_os_types}

    def create_machine_with_defaults(
        self,
        name: str,
        groups: str = "/",
        os_type_id: Optional[str] = None,
        register_machine: bool = True,
    ) -> Machine:
        """Create machine with specified name and default settings for OS type."""
        if os_type_id is None:
            os_type_id = ""
        machine = self.create_machine("", name, groups, os_type_id, "", "", "", "")
        machine.apply_defaults("")
        if register_machine:
            self.register_machine(machine)
        return machine

    def get_mediums(self, include_children: bool = False) -> list[Medium]:
        """Return list of all mediums, regardless of device type."""
        mediums = [*self.dvd_images, *self.floppy_images, *self.hard_disks]
        if include_children:
            children = []
            for medium in mediums:
                children.extend(medium.all_children)
            mediums.extend(children)
        # Remove duplicate mediums
        return list(set(mediums))

    def find_medium(self, name_or_id: str) -> Optional[Medium]:
        """Return a Medium object matching the specified name or ID, or None."""
        for medium in self.get_mediums(include_children=True):
            if name_or_id in (medium.name, medium.id):
                return medium
        return None

    def create_medium_with_defaults(
        self,
        location: str | Path,
        logical_size: int,
        format_: Optional[str] = None,
        access_mode: Medium.ACCESS_MODES_TYPE = "ReadWrite",
        device_type: Medium.DEVICE_TYPES_TYPE = "HardDisk",
    ) -> "Medium":
        """Create medium with specified location and size, with default settings."""
        location = Path(location).absolute()
        if format_ is None:
            format_ = ""
        medium = self.create_medium(format_, location, access_mode, device_type)
        medium.create_base_storage(logical_size)
        return medium
