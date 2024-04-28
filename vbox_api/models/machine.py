import base64
import functools
import io
from collections.abc import Iterator
from contextlib import contextmanager
from enum import IntEnum
from typing import Any, Callable, Literal, Optional

from PIL import Image

from vbox_api.models.base import BaseModel
from vbox_api.utils import image_to_data_uri, split_pascal_case, text_to_image


def requires_session(func: Callable) -> Callable:
    """Ensure session is open before calling wrapped function."""

    @functools.wraps(func)
    def inner(self, *args, **kwargs) -> Any:
        self.session.open()
        return func(self, *args, **kwargs)

    return inner


class MachineHealth(IntEnum):
    """Class to store simplified health status codes."""

    POWERED_OFF = 0
    RUNNING = 1
    WARNING = 2
    ERROR = 3


@BaseModel.register_model
class Machine(BaseModel):
    """Class to handle machine attributes and methods."""

    def __init__(
        self,
        ctx: "Context",
        handle: Optional["Handle"] = None,
        session: Optional["Session"] = None,
        *args,
        **kwargs,
    ) -> None:
        """Initialise base instance and add session attribute."""
        super().__init__(ctx, handle, *args, **kwargs)
        self.session = session or self.ctx.get_session()

    @requires_session
    def start(self, front_end: Literal["gui", "headless", "sdl"] = "gui") -> None:
        """Start virtual machine with specified front_end."""
        self.launch_vm_process(self.session.handle, front_end)

    @requires_session
    def stop(self) -> None:
        """Acquire lock and stop virtual machine."""
        self.lock()
        self.session.console.power_down()

    @requires_session
    def lock(self, lock_type: Literal["Write", "Shared"] = "Shared") -> "Machine":
        """Lock machine and return mutable machine instance."""
        if self.session.state == "Locked":
            return self
        self.lock_machine(self.session.handle, lock_type)
        locked_machine = self.session.get_machine()
        return Machine(self.ctx, self.ctx.get_handle(locked_machine), self.session)

    @contextmanager
    @requires_session
    def with_lock(
        self, lock_type: Literal["Write", "Shared"] = "Shared"
    ) -> Iterator["Machine"]:
        """Lock machine in a context manager and unlock on exit."""
        try:
            yield self.lock(lock_type)
        finally:
            self.session.unlock_machine()

    def get_health(self) -> tuple[str, MachineHealth]:
        """Return tuple for health of machine in format (state, status_code)."""
        match self.state:
            case "PoweredOff" | "Saved":
                health = MachineHealth.POWERED_OFF
            case "Running":
                health = MachineHealth.RUNNING
            case "Aborted":
                health = MachineHealth.ERROR
            case _:
                health = MachineHealth.WARNING
        formatted_state = split_pascal_case(self.state)
        return (formatted_state, health)

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

    def get_os_type_description(self) -> str:
        """Return description of OS type."""
        os_type = self.ctx.api.virtualbox.get_guest_os_type(self.os_type_id)
        return os_type["description"]
