from multiprocessing import Process

import websockify

from vbox_api.utils import get_available_port


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
        *args,
        **kwargs,
    ) -> tuple["WebSocketProxyProcess", str]:
        """
        Return tuple of instance of WebSocketProxyProcess and address where listening.

        Automatically assign port to random available port.
        """
        listen_port = get_available_port(listen_host)
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
        address = f"{protocol}://{listen_host}:{listen_port}"
        return (process, address)
