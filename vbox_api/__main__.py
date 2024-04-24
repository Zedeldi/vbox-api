import code
import readline
import rlcompleter
import sys
from getpass import getpass, getuser

from vbox_api import SOAPInterface, VBoxAPI

BANNER = "== Interactive VirtualBox API =="
EXITMSG = "== Exiting interactive console =="


def main() -> None:
    """Provide command-line interface to VirtualBox API."""
    interface = SOAPInterface()
    interface.connect()
    api = VBoxAPI(interface)

    if not api.login(getuser(), getpass()):
        print("Login failed.")
        sys.exit(1)

    namespace = {**globals(), **locals()}
    readline.set_completer(rlcompleter.Completer(namespace).complete)
    readline.parse_and_bind("tab: complete")
    code.InteractiveConsole(locals=namespace).interact(banner=BANNER, exitmsg=EXITMSG)


if __name__ == "__main__":
    main()
