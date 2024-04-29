import base64
import functools
import io
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from enum import IntEnum
from typing import Any, Callable, Literal, Optional

from PIL import Image

from vbox_api.models.base import BaseModel
from vbox_api.models.medium import Medium
from vbox_api.models.network import NetworkAdapter
from vbox_api.models.progress import Progress
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

    _PROPERTY_INTERFACE_ALIASES: dict[str, str] = {"NonVolatileStore": "INvramStore"}

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
    def start(self, front_end: Literal["gui", "headless", "sdl"] = "gui") -> Progress:
        """Start virtual machine with specified front_end."""
        handle = self.launch_vm_process(self.session.handle, front_end)
        return Progress(self.ctx, self.ctx.get_handle(handle))

    @requires_session
    def stop(self) -> Progress:
        """Acquire lock and stop virtual machine."""
        with self.with_lock():
            handle = self.session.console.power_down()
            return Progress(self.ctx, self.ctx.get_handle(handle))

    @requires_session
    def reset(self) -> Progress:
        """Attempt to power up and shutdown machine to remove aborted state."""
        progress = self.start()
        progress.wait_for_completion(-1)
        return self.stop()

    @requires_session
    def restart(self, front_end: Literal["gui", "headless", "sdl"] = "gui") -> Progress:
        """Stop machine and restart with specified front_end."""
        progress = self.stop()
        progress.wait_for_completion(-1)
        return self.start(front_end)

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
        self,
        lock_type: Literal["Write", "Shared"] = "Shared",
        save_on_exit: bool = False,
        force_unlock: bool = False,
    ) -> Iterator["Machine"]:
        """
        Lock machine in a context manager and conditionally unlock on exit.

        If save_on_exit is True, save_settings will be called before locking.
        If the machine is already locked, it will not be automatically unlocked,
        unless force_unlock is True.
        """
        unlock_on_exit = self.session.state != "Locked" or force_unlock
        try:
            yield self.lock(lock_type)
        finally:
            if save_on_exit:
                self.save_settings()
            if unlock_on_exit:
                self.session.unlock_machine()

    def get_mediums(self) -> list[Medium]:
        """Return list of attached mediums."""
        return [
            mapping["medium"]
            for mapping in self.medium_attachments
            if mapping["medium"]
        ]

    def get_network_adapters(
        self, slots: Iterable[int] = range(4), enabled_only: bool = True
    ) -> list[NetworkAdapter]:
        """Return list of network adapters."""
        network_adapters = [
            NetworkAdapter(
                self.ctx, self.ctx.get_handle(self.get_network_adapter(slot))
            )
            for slot in slots
        ]
        if enabled_only:
            return list(filter(lambda n: n.enabled, network_adapters))
        return network_adapters

    def get_health(self) -> MachineHealth:
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
        return health

    def get_state_name(self) -> str:
        """Return formatted machine state."""
        return split_pascal_case(self.state)

    def get_thumbnail(self, data_uri: bool = False) -> Image.Image | str:
        """
        Return thumbnail for instance of machine.

        If data_uri is True, return base64-encoded data URI.
        """
        image = self.get_running_screenshot() or self.get_saved_screenshot()
        if not image:
            image = text_to_image(self.name)
        if data_uri:
            image = image_to_data_uri(image)
        return image

    @requires_session
    def get_running_screenshot(
        self, screen_id: int = 0, bitmap_format: str = "PNG"
    ) -> Optional[Image.Image]:
        """Return screenshot of running state for screen_id if available."""
        with self.with_lock():
            try:
                info = self.session.console.display.get_screen_resolution(screen_id)
                image_b64 = self.session.console.display.take_screen_shot_to_array(
                    screen_id, info["width"], info["height"], bitmap_format
                )
                image = Image.open(io.BytesIO(base64.b64decode(image_b64)))
            except Exception:
                return None
        return image

    def get_saved_screenshot(self, screen_id: int = 0) -> Optional[Image.Image]:
        """Return screenshot of saved state for screen_id if available."""
        try:
            info = self.query_saved_screenshot_info(screen_id)
            image_dict = self.read_saved_screenshot_to_array(
                screen_id, info["returnval"][0]
            )
            image = Image.open(io.BytesIO(base64.b64decode(image_dict["returnval"])))
        except Exception:
            return None
        return image

    def get_os_type_description(self) -> str:
        """Return description of OS type."""
        os_type = self.ctx.api.virtualbox.get_guest_os_type(self.os_type_id)
        return os_type["description"]
