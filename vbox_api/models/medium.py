from pathlib import Path

from vbox_api.models.base import BaseModel
from vbox_api.utils import split_pascal_case


@BaseModel.register_model
class Medium(BaseModel):
    """Class to handle medium attributes and methods."""

    _PROPERTY_INTERFACE_ALIASES: dict[str, str] = {
        "Base": "IMedium",
        "Parent": "IMedium",
    }

    def get_path(self) -> Path:
        """Get Path instance for medium instance physical location."""
        return Path(self.location)

    def get_base_medium(self) -> "Medium":
        """Get base medium in case of snapshots."""
        if self.base.handle == self.handle:
            return self
        return self.base

    def get_parents(self, include_self: bool = False) -> list["Medium"]:
        """Recursively return parents of medium."""
        parents = [] if not include_self else [self]
        medium = self
        while parent := medium.parent:
            parents.append(parent)
            medium = parent
        return parents

    def get_device_type_name(self) -> str:
        """Return formatted device type name."""
        return split_pascal_case(self.device_type)