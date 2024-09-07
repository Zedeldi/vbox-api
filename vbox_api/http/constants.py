"""Constants for VirtualBox HTTP web application."""

from enum import Flag, auto


class UserPermission(Flag):
    """Flag enumeration for UserPermission."""

    START_VBOXWEBSRV = auto()
    READ_EVENTS = auto()
