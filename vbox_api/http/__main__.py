"""Entry-point to start Flask server."""

import sys

from vbox_api.http import app


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080


def main() -> None:
    """Parse arguments and start Flask server."""
    _, *args = sys.argv
    host, port = DEFAULT_HOST, DEFAULT_PORT

    if len(args) == 1:
        port = args[0]
    elif len(args) >= 2:
        host, port = args[0], args[1]

    app.run(host, port)


if __name__ == "__main__":
    main()
