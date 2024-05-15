from typing import Optional

from vbox_api.models.base import BaseModel, ModelRegister


class VRDEServer(BaseModel, metaclass=ModelRegister):
    """Class to handle VRDEServer attributes and methods."""

    KNOWN_EXT_PACKS: set[str] = {"Oracle VM VirtualBox Extension Pack", "VNC"}

    def get_port(self) -> Optional[int]:
        """Return port for VRDE server."""
        port = self.get_vrde_property("TCP/Ports")
        if not port:
            return None
        return int(port)

    def get_address(self) -> Optional[str]:
        """Return address for VRDE server."""
        return self.get_vrde_property("TCP/Address")

    def get_vnc_password(self) -> Optional[str]:
        """Return VNC password for VRDE server."""
        return self.get_vrde_property("VNCPassword")

    def set_port(self, port: int) -> None:
        """Set port for VRDE server."""
        return self.set_vrde_property("TCP/Ports", port)

    def set_address(self, address: str) -> None:
        """Set address for VRDE server."""
        return self.set_vrde_property("TCP/Address", address)

    def set_vnc_password(self, password: str) -> None:
        """Set VNC password for VRDE server."""
        return self.set_vrde_property("VNCPassword", password)

    def get_protocol(self) -> str:
        """Get procotol for VRDE server."""
        if self.vrde_ext_pack and self.vrde_ext_pack.upper() == "VNC":
            protocol = "VNC"
        else:
            protocol = "RDP"
        return protocol

    def get_url(self) -> Optional[str]:
        """Get URL to connect to VRDE server."""
        if not self.address:
            return None
        return f"{self.protocol.lower()}://{self.address}:{self.port}"
