"""Web interface for VirtualBox API."""

from typing import Optional

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers.response import Response

from vbox_api.helpers import WebSocketProxyProcess
from vbox_api.http import config
from vbox_api.http.session import SessionManager, requires_session

app = Flask(__name__)
app.config.from_object(config)
session_manager = SessionManager()


def get_machine_from_id(machine_id: Optional[str]) -> "Machine":
    """Return Machine instance from machine_id or abort request."""
    machine_id = machine_id or request.args.get("id")
    try:
        machine = session_manager.api.find_machine(machine_id)
    except Exception:
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
            args = dict(request.args)
            next = args.pop("next", None)
            if not next:
                return redirect(url_for("dashboard"))
            return redirect(url_for(next, **args))
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
    if request.args.get("resume", False):
        machine.resume()
    else:
        front_end = request.args.get("front_end", "headless")
        progress = machine.start(front_end)
        flash("Starting machine...", "info")
        progress.wait_for_completion(app.config["OPERATION_TIMEOUT_MS"])
    return redirect(url_for("machine", machine_id=machine.id))


@app.route("/machine/stop", methods=["GET"])
@app.route("/machine/<string:machine_id>/stop", methods=["GET"])
@requires_session(session_manager)
def machine_stop(machine_id: Optional[str] = None) -> Response | str:
    """Endpoint to stop a specified machine."""
    machine = get_machine_from_id(machine_id)
    if request.args.get("pause", False):
        machine.pause()
    elif request.args.get("reset", False):
        machine.reset()
    elif request.args.get("discard_state", False):
        machine.discard_state()
    else:
        save_state = request.args.get("save_state", False)
        progress = machine.stop(save_state=save_state)
        flash("Stopping machine...", "info")
        progress.wait_for_completion(app.config["OPERATION_TIMEOUT_MS"])
    return redirect(url_for("machine", machine_id=machine.id))


@app.route("/machine/remote", methods=["GET"])
@app.route("/machine/<string:machine_id>/remote", methods=["GET"])
@requires_session(session_manager)
def machine_remote(machine_id: Optional[str] = None) -> Response | str:
    """Endpoint to remote control a specified machine."""
    vrde_server = get_machine_from_id(machine_id).vrde_server
    if not vrde_server.address:
        abort(422, "VRDE server does not have host information.")
    if vrde_server.protocol.lower() == "vnc":
        process, address = WebSocketProxyProcess.for_address(
            vrde_server.address,
            vrde_server.port,
            listen_host=app.config["WEBSOCKET_PROXY_LISTEN_HOST"],
            web=app.config["WEBSOCKET_PROXY_VNC_PATH"],
            timeout=app.config["WEBSOCKET_PROXY_TIMEOUT"],
        )
        address = f"{address}/vnc.html"
    else:
        abort(405, f"VRDE protocol '{vrde_server.protocol}' not implemented.")
    process.start()
    return redirect(address)


@app.route("/machine/edit", methods=["GET", "POST"])
@app.route("/machine/<string:machine_id>/edit", methods=["GET", "POST"])
@requires_session(session_manager)
def machine_edit(machine_id: Optional[str] = None) -> Response | str:
    """Endpoint to edit a specified machine."""
    machine = get_machine_from_id(machine_id)
    if request.method == "POST":
        checkboxes = ("vrde_server.enabled", "vrde_server.allow_multi_connection")
        properties = dict(filter(lambda item: bool(item[1]), request.form.items()))
        for checkbox in checkboxes:
            properties[checkbox] = True if properties.get(checkbox) else False
        with machine.with_lock(
            lock_type="Write", save_settings=True
        ) as mutable_machine:
            mutable_machine.from_dict(properties)
        flash("Machine saved.", "info")
        return redirect(url_for("machine", machine_id=machine.id))
    return render_template(
        "machine_edit.html", machine=machine, api=session_manager.api
    )
