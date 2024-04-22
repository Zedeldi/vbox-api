from typing import Optional

from flask import session

from vbox_api import SOAPInterface, VBoxAPI


class SessionManager(dict):
    """Class to manage sessions and associated objects."""

    @property
    def username(self) -> Optional[str]:
        """Return username of current session."""
        return session.get("username")

    @property
    def api(self) -> Optional[VBoxAPI]:
        """Return API object associated with current username, if any."""
        api = self.get(self.username)
        if not api:
            self.logout()
        return api

    def login(self, username: str, password: str) -> bool:
        """Log in user and return status."""
        interface = SOAPInterface()
        interface.connect()
        api = VBoxAPI(interface)
        if not api.login(username, password):
            return False
        session["username"] = username
        self[username] = api
        return True

    def logout(self) -> None:
        """Log out current user."""
        username = session.pop("username", None)
        self.pop(username, None)
