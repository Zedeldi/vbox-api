import base64
import io
from typing import Literal, Optional

from PIL import Image

from vbox_api.api.handle import Handle
from vbox_api.models.base import BaseModel
from vbox_api.utils import image_to_data_uri, text_to_image


class Machine(BaseModel):
    """Class to handle machine attributes and methods."""

    def start(self, front_end: Literal["gui", "headless", "sdl"] = "gui") -> None:
        """Start virtual machine with specified front_end."""
        with self.ctx.session as session_handle:
            self.launch_vm_process(session_handle, front_end)

    def lock(self, lock_type: Literal["Write", "Shared"] = "Shared") -> "Machine":
        """Lock machine and return mutable machine instance."""
        with self.ctx.session as session_handle:
            self.lock_machine(session_handle, lock_type)
            locked_machine = self.ctx.session.get_machine()
        return Machine(self.ctx, Handle(self.ctx, locked_machine))

    def get_thumbnail(self, data_uri: bool = False) -> Image.Image | str:
        """
        Return thumbnail for instance of machine.

        If data_uri is True, return base64-encoded data URI.
        """
        image = self.get_saved_screenshot()
        if not image:
            image = text_to_image(self.name)
        if data_uri:
            image = image_to_data_uri(image)
        return image

    def get_saved_screenshot(self) -> Optional[Image.Image]:
        """Return screenshot of saved state if available."""
        try:
            info = self.query_saved_screenshot_info(0)
            image_dict = self.read_saved_screenshot_to_array(0, info["returnval"][0])
            image = Image.open(io.BytesIO(base64.b64decode(image_dict["returnval"])))
        except Exception:
            return None
        return image
