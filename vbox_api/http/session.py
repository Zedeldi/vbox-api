import functools
from typing import Callable, Optional

from flask import redirect, request, session, url_for
from werkzeug.wrappers.response import Response

from vbox_api import SOAPInterface, VBoxAPI


def requires_session(session_manager: "SessionManager") -> Callable:
    """Redirect user to login page if no active session."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def inner(*args, **kwargs) -> Response | str:
            if not session_manager.api:
                return redirect(url_for("login", next=request.endpoint, **request.args))
            return func(*args, **kwargs)

        return inner

    return decorator


class SessionManager(dict):
    """Class to manage sessions and associated API instance."""

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
