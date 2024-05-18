"""Blueprint for machine endpoints."""

from typing import Optional

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.wrappers.response import Response

from vbox_api.helpers import WebSocketProxyProcess
from vbox_api.http.session import requires_session

machine_blueprint = Blueprint("machine", __name__)


def get_machine_from_id(machine_id: Optional[str]) -> "Machine":
    """Return Machine instance from machine_id or abort request."""
    machine_id = machine_id or request.args.get("id")
    try:
        machine = g.api.find_machine(machine_id)
    except Exception:
        abort(400, "No machine specified." if not machine_id else "Machine not found.")
    return machine


@machine_blueprint.route("/", methods=["GET"])
@machine_blueprint.route("/<string:machine_id>", methods=["GET"])
@requires_session
def view(machine_id: Optional[str] = None) -> Response | str:
    """Endpoint to view and manage a specified machine."""
    machine = get_machine_from_id(machine_id)
    return render_template("machine/view.html", machine=machine)


@machine_blueprint.route("/start", methods=["GET"])
@machine_blueprint.route("/<string:machine_id>/start", methods=["GET"])
@requires_session
def start(machine_id: Optional[str] = None) -> Response | str:
    """Endpoint to start a specified machine."""
    machine = get_machine_from_id(machine_id)
    if request.args.get("resume", False):
        machine.resume()
    else:
        front_end = request.args.get("front_end", "headless")
        progress = machine.start(front_end)
        flash("Starting machine...", "info")
        progress.wait_for_completion(current_app.config["OPERATION_TIMEOUT_MS"])
    return redirect(url_for("machine.view", machine_id=machine.id))


@machine_blueprint.route("/stop", methods=["GET"])
@machine_blueprint.route("/<string:machine_id>/stop", methods=["GET"])
@requires_session
def stop(machine_id: Optional[str] = None) -> Response | str:
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
        progress.wait_for_completion(current_app.config["OPERATION_TIMEOUT_MS"])
    return redirect(url_for("machine.view", machine_id=machine.id))


@machine_blueprint.route("/remote", methods=["GET"])
@machine_blueprint.route("/<string:machine_id>/remote", methods=["GET"])
@requires_session
def remote(machine_id: Optional[str] = None) -> Response | str:
    """Endpoint to remote control a specified machine."""
    vrde_server = get_machine_from_id(machine_id).vrde_server
    if not vrde_server.address:
        abort(422, "VRDE server does not have host information.")
    if vrde_server.protocol.lower() == "vnc":
        process, address = WebSocketProxyProcess.for_address(
            vrde_server.address,
            vrde_server.port,
            listen_host=current_app.config["WEBSOCKET_PROXY_LISTEN_HOST"],
            web=current_app.config["WEBSOCKET_PROXY_VNC_PATH"],
            timeout=current_app.config["WEBSOCKET_PROXY_TIMEOUT"],
        )
        address = f"{address}/vnc.html"
    else:
        abort(405, f"VRDE protocol '{vrde_server.protocol}' not implemented.")
    process.start()
    return redirect(address)


@machine_blueprint.route("/edit", methods=["GET", "POST"])
@machine_blueprint.route("/<string:machine_id>/edit", methods=["GET", "POST"])
@requires_session
def edit(machine_id: Optional[str] = None) -> Response | str:
    """Endpoint to edit a specified machine."""
    machine = get_machine_from_id(machine_id)
    if request.method == "POST":
        checkboxes = ("vrde_server.enabled", "vrde_server.allow_multi_connection")
        properties: dict[str, str | bool] = dict(
            filter(lambda item: bool(item[1]), request.form.items())
        )
        for checkbox in checkboxes:
            properties[checkbox] = True if properties.get(checkbox) else False
        with machine.with_lock(
            lock_type="Write", save_settings=True
        ) as mutable_machine:
            mutable_machine.from_dict(properties)
        flash("Machine saved.", "info")
        return redirect(url_for("machine.view", machine_id=machine.id))
    return render_template("machine/edit.html", machine=machine, api=g.api)


@machine_blueprint.route("/delete", methods=["GET"])
@machine_blueprint.route("/<string:machine_id>/delete", methods=["GET"])
@requires_session
def delete(machine_id: Optional[str] = None) -> Response | str:
    """Endpoint to delete a specified machine."""
    machine = get_machine_from_id(machine_id)
    progress = machine.delete(delete_config=True)
    flash("Deleting machine...", "warning")
    progress.wait_for_completion(current_app.config["OPERATION_TIMEOUT_MS"])
    return redirect(url_for("dashboard"))
