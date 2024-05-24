import random
import string
from getpass import getpass, getuser

import pytest

from vbox_api import SOAPInterface, VBoxAPI
from vbox_api.models import Machine

interface = SOAPInterface()
interface.connect()
vbox_api = VBoxAPI(interface)
assert vbox_api.login(getuser(), getpass())


@pytest.fixture(scope="session")
def api() -> VBoxAPI:
    """Return VBoxAPI instance."""
    return vbox_api


@pytest.fixture
def random_machine(api: VBoxAPI) -> Machine:
    """Return random machine of API."""
    return random.choice(api.machines)


@pytest.fixture
def random_string() -> str:
    """Return random string."""
    "".join(random.choice(string.ascii_letters) for _ in range(32))
