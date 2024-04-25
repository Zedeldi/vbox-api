"""Web interface for VirtualBox API."""

from typing import Optional

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers.response import Response

from vbox_api.http import config
from vbox_api.http.session import SessionManager, requires_session
from vbox_api.models.machine import Machine

app = Flask(__name__)
app.config.from_object(config)
session_manager = SessionManager()


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


@app.route("/machine", methods=["GET", "POST"])
@app.route("/machine/<string:machine_id>", methods=["GET", "POST"])
@requires_session(session_manager)
def machine(machine_id: Optional[str] = None) -> Response | str:
    """Endpoint to view and manage a specified machine."""
    machine_id = machine_id or request.args.get("id")
    machine = session_manager.api.find_machine(machine_id)
    if not machine:
        abort(400, "No machine specified." if not machine_id else "Machine not found.")
    return render_template("machine.html", machine=machine)
