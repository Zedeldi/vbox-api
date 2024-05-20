import base64
import functools
import io
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from datetime import datetime
from enum import IntEnum
from typing import Any, Callable, Literal, Optional

from PIL import Image

from vbox_api import api
from vbox_api.models.base import BaseModel, ModelRegister
from vbox_api.models.medium import Medium
from vbox_api.models.network import NetworkAdapter
from vbox_api.models.progress import Progress
from vbox_api.models.session import Session
from vbox_api.utils import image_to_data_uri, split_pascal_case, text_to_image


def requires_session(func: Callable) -> Callable:
    """Ensure session is open before calling wrapped function."""

    @functools.wraps(func)
    def inner(self: "Machine", *args, **kwargs) -> Any:
        self.session.open()
        return func(self, *args, **kwargs)

    return inner


class MachineHealth(IntEnum):
    """Class to store simplified health status codes."""

    POWERED_OFF = 0
    RUNNING = 1
    WARNING = 2
    ERROR = 3


class Machine(BaseModel, metaclass=ModelRegister):
    """Class to handle machine attributes and methods."""

    _PROPERTY_INTERFACE_ALIASES: dict[str, str] = {"NonVolatileStore": "INvramStore"}

    def __init__(
        self,
        ctx: "api.Context",
        handle: Optional["api.Handle"] = None,
        session: Optional[Session] = None,
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
        return self.ctx.get_progress(handle)

    @requires_session
    def stop(self, save_state: bool = False) -> Progress:
        """
        Acquire lock and stop virtual machine.

        If save_state is True, save machine state and power down.
        """
        with self.with_lock():
            if save_state:
                handle = self.session.machine.save_state()
            else:
                handle = self.session.console.power_down()
            return self.ctx.get_progress(handle)

    @requires_session
    def discard_state(self, remove_file: bool = True) -> None:
        """Acquire lock and discard saved state of machine."""
        with self.with_lock():
            self.session.machine.discard_saved_state(remove_file)

    @requires_session
    def reset(self) -> None:
        """Acquire lock and forcefully reset machine."""
        with self.with_lock():
            self.session.console.reset()

    @requires_session
    def restart(self, front_end: Literal["gui", "headless", "sdl"] = "gui") -> Progress:
        """Stop machine and restart with specified front_end."""
        progress = self.stop()
        progress.wait_for_completion(-1)
        return self.start(front_end)

    @requires_session
    def pause(self) -> None:
        """Pause machine execution state."""
        with self.with_lock():
            self.session.console.pause()

    @requires_session
    def resume(self) -> None:
        """Resume machine execution state."""
        with self.with_lock():
            self.session.console.resume()

    @requires_session
    def fix_state(self) -> Progress:
        """Attempt to power up and shutdown machine to remove aborted state."""
        try:
            progress = self.start()
            progress.wait_for_completion(-1)
        except Exception:
            pass
        return self.stop()

    @requires_session
    def lock(self, lock_type: Literal["Write", "Shared"] = "Shared") -> "Machine":
        """Lock machine and return mutable machine instance."""
        if self.session.state == "Locked":
            return self.session.machine
        self.lock_machine(self.session.handle, lock_type)
        locked_machine = self.session.get_machine()
        locked_machine.session = self.session
        return locked_machine

    @requires_session
    def unlock(self, save_settings: bool = False) -> None:
        """Unlock machine and optionally save settings."""
        if save_settings:
            self.session.machine.save_settings()
        self.session.unlock_machine()

    @contextmanager
    @requires_session
    def with_lock(
        self,
        lock_type: Literal["Write", "Shared"] = "Shared",
        save_settings: bool = False,
        force_unlock: bool = False,
    ) -> Iterator["Machine"]:
        """
        Lock machine in a context manager and conditionally unlock on exit.

        If save_settings is True, save_settings will be called before unlocking.
        If the machine is already locked, it will not be automatically unlocked,
        unless force_unlock is True.
        """
        unlock_on_exit = self.session.state != "Locked" or force_unlock
        try:
            yield self.lock(lock_type)
        finally:
            if save_settings:
                self.session.machine.save_settings()
            if unlock_on_exit:
                self.unlock()

    def delete(
        self,
        cleanup_mode: Literal[
            "UnregisterOnly",
            "DetachAllReturnNone",
            "DetachAllReturnHardDisksOnly",
            "Full",
        ] = "DetachAllReturnHardDisksOnly",
        delete_config: bool = True,
    ) -> Optional[Progress]:
        """Delete and unregister machine with specified cleanup mode."""
        media = self.unregister(cleanup_mode)
        if not delete_config:
            return None
        handle = self.delete_config(media)
        return self.ctx.get_progress(handle)

    def attach_medium(
        self,
        medium: Medium,
        controller_name: str,
        controller_port: Optional[int] = None,
        controller_device: int = 0,
    ) -> None:
        """Attach medium to controller at next available port, unless specified."""
        if controller_port is None:
            controller_port = self._get_next_port_for_storage_controller(
                controller_name
            )
        with self.with_lock(save_settings=True) as locked_machine:
            locked_machine.attach_device(
                controller_name,
                controller_port,
                controller_device,
                medium.device_type,
                medium,
            )

    def detach_medium(self, medium: Medium) -> None:
        """Find storage controller for medium and detach medium."""
        storage_controller = self._find_storage_controller_for_medium(medium)
        if not storage_controller:
            raise ValueError(f"Cannot find storage controller for medium {medium.id}")
        with self.with_lock(save_settings=True) as locked_machine:
            locked_machine.detach_device(*storage_controller)

    def _find_storage_controller_for_medium(
        self, medium: Medium
    ) -> Optional[tuple[str, int, int]]:
        """Return storage controller name, port and device for medium."""
        for medium_attachment in self.medium_attachments:
            if medium_attachment.medium == medium:
                return (
                    medium_attachment.controller,
                    medium_attachment.port,
                    medium_attachment.device,
                )
        return None

    def _get_available_ports_for_storage_controller(
        self, controller_name: str
    ) -> set[int]:
        """Return set of available ports for storage controller."""
        storage_controller = self.get_storage_controller_by_name(controller_name)
        medium_attachments = self.get_medium_attachments_of_controller(
            storage_controller.name
        )
        ports_in_use = {attachment.port for attachment in medium_attachments}
        # Ports are zero-indexed, but port_count starts at one
        return set(range(0, storage_controller.port_count)) - set(ports_in_use)

    def _get_next_port_for_storage_controller(self, controller_name: str) -> int:
        """Return next available port for storage controller, increasing port_count if necessary."""
        while not (
            available_ports := self._get_available_ports_for_storage_controller(
                controller_name
            )
        ):
            with self.with_lock(save_settings=True) as locked_machine:
                storage_controller = locked_machine.get_storage_controller_by_name(
                    controller_name
                )
                storage_controller.port_count += 1
        return min(available_ports)

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
        network_adapters = [self.get_network_adapter(slot) for slot in slots]
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
        try:
            with self.with_lock():
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
        os_type = self.ctx.api.get_guest_os_type(self.os_type_id)
        return os_type.description

    def get_last_state_change_dt(self) -> datetime:
        """Return datetime object for last state change."""
        return datetime.fromtimestamp(self.last_state_change / 1000)
