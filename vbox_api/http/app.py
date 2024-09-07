"""Flask application for VirtualBox API web interface."""

import logging

import requests.exceptions
from flask import Flask, abort, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers.response import Response

from vbox_api import constants, utils
from vbox_api.helpers import start_vboxwebsrv
from vbox_api.http import config
from vbox_api.http.constants import UserPermission
from vbox_api.http.session import SessionManager, requires_session
from vbox_api.http.utils import is_allowed
from vbox_api.http.views import blueprints

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
api_filter = logging.Filter("vbox_api")
file_handler.addFilter(api_filter)
logging.basicConfig(
    format="%(asctime)s | [%(levelname)s] %(message)s",
    level=config.LOG_LEVEL,
    handlers=[
        file_handler,
        logging.StreamHandler(),
    ],
)

app = Flask(__name__)
app.config.from_object(config)

for url_prefix, blueprint in blueprints.items():
    app.register_blueprint(blueprint, url_prefix=url_prefix)

session_manager = SessionManager()


@app.before_request
def load_session() -> None:
    """Initialise Flask global application context object."""
    g.session_manager = session_manager
    g.api = session_manager.api
    g.username = session_manager.username
    g.constants = constants
    g.permissions = UserPermission
    g.is_allowed = is_allowed


@app.errorhandler(HTTPException)
def handle_exception(error: HTTPException) -> tuple[str, int]:
    """Handle HTTP errors."""
    return render_template("error.html", error=error), error.code


@app.route("/", methods=["GET"])
@requires_session
def dashboard() -> Response | str:
    """Endpoint for dashboard."""
    return render_template("dashboard.html", machines=g.api.machines, utils=utils)


@app.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
    """Endpoint to login to interface."""
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        host = (
            request.form.get("host") or "localhost",
            request.form.get("port") or 18083,
        )
        try:
            if not session_manager.login(username, password, host=host):
                logger.error(f"Authentication failed for user '{username}'")
                flash("Incorrect username or password.", "danger")
            else:
                logger.info(f"User '{username}' has logged in")
                args = dict(request.args)
                next_endpoint = args.pop("next", None)
                if not next_endpoint:
                    return redirect(url_for("dashboard"))
                return redirect(url_for(next_endpoint, **args))
        except requests.exceptions.ConnectionError:
            flash("Could not connect to server.", "danger")
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout() -> Response:
    """Endpoint to log out current session."""
    logger.info(f"User '{session_manager.username}' has logged out")
    session_manager.logout()
    return redirect(url_for("dashboard"))


@app.route("/events", methods=["GET"])
@requires_session
def events() -> Response:
    """Endpoint to display events."""
    if not is_allowed(UserPermission.READ_EVENTS):
        abort(403, "Reading events is not allowed by the server.")
    try:
        with open(config.LOG_FILE, "r") as fd:
            data = fd.read()
    except FileNotFoundError:
        abort(404, "Log file not found.")
    # Strip ANSI escape codes in case log includes console output
    events = list(filter(bool, map(utils.strip_ansi, reversed(data.split("\n")))))
    return render_template("events.html", events=events)


@app.route("/vboxwebsrv", methods=["GET"])
def vboxwebsrv() -> Response:
    """Endpoint to start vboxwebsrv on host."""
    if not is_allowed(UserPermission.START_VBOXWEBSRV):
        abort(403, "Starting vboxwebsrv is not allowed by the server.")
    logger.info("Starting 'vboxwebsrv' with default arguments")
    flash("Starting Oracle VM VirtualBox web service...", "info")
    start_vboxwebsrv()
    return redirect(request.referrer)
