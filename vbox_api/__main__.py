import code
from getpass import getpass, getuser

from vbox_api import SOAPInterface, VBoxAPI

BANNER = "== Interactive VirtualBox API =="
EXITMSG = "== Exiting interactive console =="


def main() -> None:
    """Provide command-line interface to VirtualBox API."""
    interface = SOAPInterface()
    interface.connect()
    api = VBoxAPI(interface)

    username, password = getuser(), getpass()
    api.login(username, password)

    code.InteractiveConsole(locals={"api": api}).interact(
        banner=BANNER, exitmsg=EXITMSG
    )


if __name__ == "__main__":
    main()
