"""
Command-line interface to the VirtualBox API via an InteractiveConsole.

Available objects:
 - built-ins
 - api: VBoxAPI
 - interface: SOAPInterface
"""

import code
import readline
import rlcompleter
import sys
import time
from getpass import getpass, getuser

import requests.exceptions

from vbox_api import SOAPInterface, VBoxAPI
from vbox_api.cli.args import get_parser
from vbox_api.helpers import start_vboxwebsrv

BANNER = "== Interactive VirtualBox API =="
EXITMSG = "== Exiting interactive console =="


def main() -> None:
    """Provide command-line interface to VirtualBox API."""
    parser = get_parser()
    args = parser.parse_args()

    if args.vboxwebsrv:
        start_vboxwebsrv()

    interface = SOAPInterface(args.host, args.port)
    for _ in range(args.attempts):
        try:
            interface.connect()
            break
        except requests.exceptions.ConnectionError:
            time.sleep(args.interval)
    else:
        print(
            f"Connection to {args.host}:{args.port} failed "
            f"after {args.attempts} attempts."
        )
        print("Check if vboxwebsrv is running on the host.")
        sys.exit(1)

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
