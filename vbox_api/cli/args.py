"""Handle arguments for command-line interface.."""

from argparse import ArgumentParser


def get_parser() -> ArgumentParser:
    """Return argument parser instance."""
    parser = ArgumentParser(
        prog="vbox_api",
        description="Python command-line interface for VirtualBox API",
        epilog="Copyright (C) 2025 Zack Didcott",
    )

    parser.add_argument(
        "--host", "-H", type=str, default="127.0.0.1", help="host for SOAP interface"
    )
    parser.add_argument(
        "--port", "-p", type=int, default=18083, help="port for SOAP interface"
    )
    parser.add_argument(
        "--vboxwebsrv", action="store_true", help="start vboxwebsrv in the background"
    )
    parser.add_argument(
        "--interval",
        "-i",
        type=int,
        default=1,
        help="interval between connection attempts (in seconds)",
    )
    parser.add_argument(
        "--attempts",
        "-a",
        type=int,
        default=3,
        help="maximum number of connection attempts",
    )

    return parser
