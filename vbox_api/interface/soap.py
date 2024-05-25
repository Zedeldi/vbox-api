"""SOAP interface implementation to VirtualBox API."""

from pathlib import Path
from typing import Optional

import requests
import zeep
from lxml import etree

from vbox_api.interface.base import BaseInterface, ProxyInterface


class SOAPInterface(BaseInterface):
    """Define interface class for SOAP methods."""

    BINDING_QNAME = "{http://www.virtualbox.org/}vboxBinding"
    TYPES_QNAME = "{http://schemas.xmlsoap.org/wsdl/}types"
    SCHEMA_QNAME = "{http://www.w3.org/2001/XMLSchema}schema"
    SIMPLETYPE_QNAME = "{http://www.w3.org/2001/XMLSchema}simpleType"
    RESTRICTION_QNAME = "{http://www.w3.org/2001/XMLSchema}restriction"
    ENUMERATION_QNAME = "{http://www.w3.org/2001/XMLSchema}enumeration"

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
            raise RuntimeError("Service has not yet been created")
        for operation, method_callable in self.service._operations.items():
            interface_name, method_name = operation.split("_")
            if (proxy_interface := getattr(self, interface_name, None)) is None:
                proxy_interface = ProxyInterface()
                self._register_interface(interface_name, proxy_interface)
            proxy_interface._register_method(method_name, method_callable)

    def get_enums(self, path: Optional[str | Path] = None) -> dict[str, list[str]]:
        """Return dictionary of enums in WSDL document."""
        if path:
            with open(path) as fd:
                wsdl = etree.parse(fd)
            root = wsdl.getroot()
        else:
            wsdl = requests.get(self.wsdl).content
            root = etree.fromstring(wsdl)
        schema = root.find(self.TYPES_QNAME).find(self.SCHEMA_QNAME)
        return {
            element.get("name"): [
                enum.get("value")
                for enum in element.find(self.RESTRICTION_QNAME).findall(
                    self.ENUMERATION_QNAME
                )
            ]
            for element in schema.findall(self.SIMPLETYPE_QNAME)
        }
