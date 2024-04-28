"""Web interface for VirtualBox API."""

from typing import Optional

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers.response import Response

from vbox_api.http import config
from vbox_api.http.session import SessionManager, requires_session

app = Flask(__name__)
app.config.from_object(config)
session_manager = SessionManager()


def get_machine_from_id(machine_id: Optional[str]) -> "Machine":
    """Return Machine instance from machine_id or abort request."""
    machine_id = machine_id or request.args.get("id")
    machine = session_manager.api.find_machine(machine_id)
    if not machine:
        abort(400, "No machine specified." if not machine_id else "Machine not found.")
    return machine


@app.errorhandler(HTTPException)
def handle_exception(error: HTTPException) -> tuple[str, int]:
    """Handle HTTP errors."""
    return render_template("error.html", error=error), error.code


@app.route("/", methods=["GET"])
@requires_session(session_manager)
def dashboard() -> Response | str:
    """Endpoint for dashboard."""
    return render_template("dashboard.html", machines=session_manager.api.machines)


@app.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
    """Endpoint to login to interface."""
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        if not session_manager.login(username, password):
            flash("Incorrect username or password.", "danger")
        else:
            url = url_for(request.args.get("next", "dashboard"))
            return redirect(url)
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout() -> Response:
    """Endpoint to log out current session."""
    session_manager.logout()
    return redirect(url_for("dashboard"))


@app.route("/machine", methods=["GET"])
@app.route("/machine/<string:machine_id>", methods=["GET"])
@requires_session(session_manager)
def machine(machine_id: Optional[str] = None) -> Response | str:
    """Endpoint to view and manage a specified machine."""
    machine = get_machine_from_id(machine_id)
    return render_template("machine.html", machine=machine)


@app.route("/machine/start", methods=["GET"])
@app.route("/machine/<string:machine_id>/start", methods=["GET"])
@requires_session(session_manager)
def machine_start(machine_id: Optional[str] = None) -> Response | str:
    """Endpoint to start a specified machine."""
    machine = get_machine_from_id(machine_id)
    front_end = request.args.get("front_end", "headless")
    machine.start(front_end)
    return redirect(url_for("machine", machine_id=machine.id))


@app.route("/machine/stop", methods=["GET"])
@app.route("/machine/<string:machine_id>/stop", methods=["GET"])
@requires_session(session_manager)
def machine_stop(machine_id: Optional[str] = None) -> Response | str:
    """Endpoint to stop a specified machine."""
    machine = get_machine_from_id(machine_id)
    machine.session.console.power_down()
    return redirect(url_for("machine", machine_id=machine.id))
