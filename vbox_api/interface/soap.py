from typing import Optional

import zeep

from vbox_api.interface.base import BaseInterface, ProxyInterface


class SOAPInterface(BaseInterface):
    """Define interface class for SOAP methods."""

    BINDING_QNAME = "{http://www.virtualbox.org/}vboxBinding"

    def __init__(self, host: str = "localhost", port: int = 18083) -> None:
        """Initialise instance of interface."""
        self.host = host
        self.port = port
        self.url = f"http://{self.host}:{self.port}"
        self.wsdl = f"{self.url}/?wsdl"
        self.client: Optional[zeep.Client] = None
        self.service: Optional[zeep.proxy.ServiceProxy] = None

    def connect(self) -> None:
        """Connect to VirtualBox web service."""
        self.client = zeep.Client(self.wsdl)
        self.service = self.client.create_service(self.BINDING_QNAME, self.url)
        self._register_methods()

    def _register_methods(self) -> None:
        """Add methods from SOAP service to instance."""
        if not self.service:
            raise RuntimeError("Service has not yet been created.")
        for operation, method_callable in self.service._operations.items():
            interface_name, method_name = operation.split("_")
            if (proxy_interface := getattr(self, interface_name, None)) is None:
                proxy_interface = ProxyInterface()
                setattr(self, interface_name, proxy_interface)
            proxy_interface.__setattr__(method_name, method_callable)
