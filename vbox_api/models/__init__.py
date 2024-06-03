"""
Collection of models with additional methods and properties.

Other models will be generated dynamically at runtime by name
using an interface instance.
"""

from vbox_api.models.audio import AudioSettings
from vbox_api.models.event import (
    Event,
    EventListener,
    EventListenerLoop,
    EventSource,
    PassiveEventListener,
)
from vbox_api.models.machine import Machine
from vbox_api.models.medium import Medium
from vbox_api.models.network import NetworkAdapter
from vbox_api.models.progress import Progress
from vbox_api.models.session import Session
from vbox_api.models.unattended import Unattended
from vbox_api.models.virtualbox import VirtualBox
from vbox_api.models.vrde import VRDEServer

__all__ = [
    "AudioSettings",
    "Event",
    "EventListener",
    "EventListenerLoop",
    "EventSource",
    "Machine",
    "Medium",
    "NetworkAdapter",
    "PassiveEventListener",
    "Progress",
    "Session",
    "Unattended",
    "VirtualBox",
    "VRDEServer",
]
