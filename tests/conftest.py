import random
import string
from getpass import getpass, getuser

import pytest
from flask import Flask
from flask.testing import FlaskClient

from vbox_api import SOAPInterface, VBoxAPI
from vbox_api.http import app as http_app
from vbox_api.models import Machine

interface = SOAPInterface()
interface.connect()
vbox_api = VBoxAPI(interface)
assert vbox_api.login(getuser(), getpass())

http_app.config.update({"TESTING": True})


@pytest.fixture(scope="session")
def api() -> VBoxAPI:
    """Return VBoxAPI instance."""
    return vbox_api


@pytest.fixture()
def app() -> Flask:
    """Return Flask application."""
    return http_app


@pytest.fixture()
def client(app) -> FlaskClient:
    """Return Flask test client."""
    return app.test_client()


@pytest.fixture
def random_machine(api: VBoxAPI) -> Machine:
    """Return random machine of API."""
    return random.choice(api.machines)


@pytest.fixture
def random_string() -> str:
    """Return random string."""
    "".join(random.choice(string.ascii_letters) for _ in range(32))
