"""Collection of helpers for external modules for integration with VirtualBox API."""

import os
import subprocess
from multiprocessing import Process
from typing import Optional

import psutil
import websockify

from vbox_api.utils import get_available_port, get_fqdn


def get_vboxwebsrv_process(*args, **kwargs) -> Optional[psutil.Process]:
    """Return process for vboxwebsrv, if running."""
    for proc in psutil.process_iter():
        if "vboxwebsrv" == proc.name().lower():
            return proc
    return None


def start_vboxwebsrv(*args, **kwargs) -> Optional[subprocess.Popen]:
    """Start vboxwebsrv with specified arguments."""
    if get_vboxwebsrv_process():
        return None

    vboxwebsrv = (
        r"C:\Program Files\Oracle\VirtualBox\VBoxWebSrv.exe"
        if os.name == "nt"
        else "/usr/bin/vboxwebsrv"
    )
    return subprocess.Popen(
        [vboxwebsrv, *args],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        **kwargs,
    )


class WebSocketProxyProcess(Process):
    """Helper class to handle WebSocketProxy in a separate process."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialise self and WebSocketProxy instance."""
        self._websocket_proxy = websockify.WebSocketProxy(*args, **kwargs)
        super().__init__(target=self._websocket_proxy.start_server)

    @classmethod
    def for_address(
        cls: "WebSocketProxyProcess",
        target_host: str,
        target_port: int,
        listen_host: str = "0.0.0.0",
        listen_port: int = 0,
        *args,
        **kwargs,
    ) -> tuple["WebSocketProxyProcess", str]:
        """
        Return tuple of instance of WebSocketProxyProcess and address where listening.

        If listen_port is 0, automatically assign port to random available port.
        """
        listen_port = (
            get_available_port(listen_host) if listen_port == 0 else listen_port
        )
        process = cls(
            target_host=target_host,
            target_port=target_port,
            listen_host=listen_host,
            listen_port=listen_port,
            *args,
            **kwargs,
        )
        if "cert" in kwargs.keys():
            protocol = "https"
        else:
            protocol = "http"
        if listen_host == "0.0.0.0":
            listen_host = get_fqdn()
        address = f"{protocol}://{listen_host}:{listen_port}"
        return (process, address)
