import base64
import functools
import io
from typing import Any, Callable, Literal, Optional

from PIL import Image

from vbox_api.api.handle import Handle
from vbox_api.models.base import BaseModel
from vbox_api.utils import image_to_data_uri, text_to_image


def requires_session(func: Callable) -> Callable:
    """Decorator to ensure session is open."""

    @functools.wraps(func)
    def inner(self, *args, **kwargs) -> Any:
        self.session.open()
        return func(self, *args, **kwargs)

    return inner


class Machine(BaseModel):
    """Class to handle machine attributes and methods."""

    def __init__(
        self,
        ctx: "Context",
        handle: Optional["Handle"] = None,
        session: Optional["Session"] = None,
    ) -> None:
        """Initialise base instance and add session attribute."""
        super().__init__(ctx, handle)
        self.session = session or self.ctx.get_session()

    @requires_session
    def start(self, front_end: Literal["gui", "headless", "sdl"] = "gui") -> None:
        """Start virtual machine with specified front_end."""
        self.launch_vm_process(self.session.handle, front_end)

    @requires_session
    def lock(self, lock_type: Literal["Write", "Shared"] = "Shared") -> "Machine":
        """Lock machine and return mutable machine instance."""
        self.lock_machine(self.session.handle, lock_type)
        locked_machine = self.session.get_machine()
        return Machine(self.ctx, Handle(self.ctx, locked_machine), self.session)

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
