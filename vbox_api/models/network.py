from typing import Optional

from vbox_api.models.base import BaseModel
from vbox_api.utils import split_pascal_case


@BaseModel.register_model
class NetworkAdapter(BaseModel):
    """Class to handle NetworkAdapter attributes and methods."""

    def get_attachment_type_name(self) -> str:
        """Return formatted attachment type name."""
        return split_pascal_case(self.attachment_type)

    def get_interface_name(self) -> Optional[str]:
        """Get interface name for attachment type."""
        attachment_type = self.get_attachment_type_name().lower().replace(" ", "_")
        try:
            return getattr(self, f"{attachment_type}_interface")
        except AttributeError:
            return None
