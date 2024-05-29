from pathlib import Path

from vbox_api.models.base import BaseModel, ModelRegister
from vbox_api.utils import split_pascal_case


class Medium(BaseModel, metaclass=ModelRegister):
    """Class to handle medium attributes and methods."""

    def get_path(self) -> Path:
        """Get Path instance for medium instance physical location."""
        return Path(self.location).absolute()

    def get_parents(self, include_self: bool = False) -> list["Medium"]:
        """Return parents of medium iteratively."""
        parents = [] if not include_self else [self]
        medium = self
        while parent := medium.parent:
            parents.append(parent)
            medium = parent
        return parents

    def get_all_children(self) -> list["Medium"]:
        """Return a flat list of all children of medium recursively."""
        if not self.children:  # Base case
            return [self]
        children = []
        for child in self.children:
            children.extend(child.get_all_children())
        return children

    def get_device_type_name(self) -> str:
        """Return formatted device type name."""
        return split_pascal_case(self.device_type)
