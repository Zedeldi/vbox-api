"""Blueprint for machine endpoints."""

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
from vbox_api.http.utils import convert_id_to_model
from vbox_api.models import Machine

machine_blueprint = Blueprint("machine", __name__)


@machine_blueprint.route("/", methods=["GET"])
@requires_session
def overview() -> Response | str:
    """Endpoint to view all machines."""
    return render_template("machine/overview.html")


@machine_blueprint.route("/view", methods=["GET"])
@machine_blueprint.route("/<string:name_or_id>", methods=["GET"])
@requires_session
@convert_id_to_model("machine")
def view(machine: Machine) -> Response | str:
    """Endpoint to view and manage a specified machine."""
    return render_template("machine/view.html", machine=machine)


@machine_blueprint.route("/start", methods=["GET"])
@machine_blueprint.route("/<string:name_or_id>/start", methods=["GET"])
@requires_session
@convert_id_to_model("machine")
def start(machine: Machine) -> Response | str:
    """Endpoint to start a specified machine."""
    if request.args.get("resume", False):
        machine.resume()
    else:
        front_end = request.args.get("front_end", "headless")
        progress = machine.start(front_end)
        flash("Starting machine...", "info")
        progress.wait_for_completion(current_app.config["OPERATION_TIMEOUT_MS"])
    return redirect(url_for("machine.view", id=machine.id))


@machine_blueprint.route("/stop", methods=["GET"])
@machine_blueprint.route("/<string:name_or_id>/stop", methods=["GET"])
@requires_session
@convert_id_to_model("machine")
def stop(machine: Machine) -> Response | str:
    """Endpoint to stop a specified machine."""
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
    return redirect(url_for("machine.view", id=machine.id))


@machine_blueprint.route("/remote", methods=["GET"])
@machine_blueprint.route("/<string:name_or_id>/remote", methods=["GET"])
@requires_session
@convert_id_to_model("machine")
def remote(machine: Machine) -> Response | str:
    """Endpoint to remote control a specified machine."""
    vrde_server = machine.vrde_server
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
@machine_blueprint.route("/<string:name_or_id>/edit", methods=["GET", "POST"])
@requires_session
@convert_id_to_model("machine")
def edit(machine: Machine) -> Response | str:
    """Endpoint to edit a specified machine."""
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
        return redirect(url_for("machine.view", id=machine.id))
    return render_template("machine/edit.html", machine=machine)


@machine_blueprint.route("/medium", methods=["GET"])
@machine_blueprint.route("/<string:name_or_id>/medium", methods=["GET"])
@requires_session
@convert_id_to_model("machine")
def medium(machine: Machine) -> Response | str:
    """Endpoint to manage mediums for a specified machine."""
    return render_template("machine/medium.html", machine=machine)


@machine_blueprint.route("/attach-medium", methods=["GET", "POST"])
@machine_blueprint.route("/<string:name_or_id>/attach-medium", methods=["GET", "POST"])
@requires_session
@convert_id_to_model("machine")
def attach_medium(machine: Machine) -> Response | str:
    """Endpoint to attach a medium to a specified machine."""
    storage_controller = request.args.get("storage_controller") or request.form.get(
        "storage_controller"
    )
    if not storage_controller:
        abort(400, "No storage controller name provided.")
    medium_id = request.args.get("medium_id") or request.form.get("medium_id")
    if not medium_id:
        abort(400, "No medium ID provided.")
    medium = g.api.find_medium(medium_id)
    if not medium:
        abort(400, f"Medium with ID {medium_id} not found.")
    machine.attach_medium(medium, storage_controller)
    flash("Medium attached.", "info")
    return redirect(url_for("machine.medium", id=machine.id))


@machine_blueprint.route("/detach-medium", methods=["GET"])
@machine_blueprint.route("/<string:name_or_id>/detach-medium", methods=["GET"])
@requires_session
@convert_id_to_model("machine")
def detach_medium(machine: Machine) -> Response | str:
    """Endpoint to detach a medium from a specified machine."""
    medium_id = request.args.get("medium_id")
    if not medium_id:
        abort(400, "No medium ID provided.")
    medium = g.api.find_medium(medium_id)
    if not medium:
        abort(400, f"Medium with ID {medium_id} not found.")
    machine.detach_medium(medium)
    flash("Medium detached.", "info")
    return redirect(url_for("machine.medium", id=machine.id))


@machine_blueprint.route("/delete", methods=["GET"])
@machine_blueprint.route("/<string:name_or_id>/delete", methods=["GET"])
@requires_session
@convert_id_to_model("machine")
def delete(machine: Machine) -> Response | str:
    """Endpoint to delete a specified machine."""
    progress = machine.delete(delete_config=True)
    flash("Deleting machine...", "warning")
    progress.wait_for_completion(current_app.config["OPERATION_TIMEOUT_MS"])
    return redirect(url_for("machine.overview"))


@machine_blueprint.route("/clone", methods=["GET"])
@machine_blueprint.route("/<string:name_or_id>/clone", methods=["GET"])
@requires_session
@convert_id_to_model("machine")
def clone(machine: Machine) -> Response | str:
    """Endpoint to clone a specified machine."""
    cloned_machine = machine.clone(f"{machine.name} - Clone")
    flash("Cloned machine.", "info")
    return redirect(url_for("machine.view", id=cloned_machine.id))


@machine_blueprint.route("/create", methods=["GET", "POST"])
@requires_session
def create() -> Response | str:
    """Endpoint to create a new machine."""
    if request.method == "POST":
        name = request.form.get("name")
        groups = request.form.get("groups", "/")
        os_type_id = request.form.get("os_type_id", None)
        machine = g.api.create_machine_with_defaults(name, groups, os_type_id)
        return redirect(url_for("machine.edit", id=machine.id))
    return render_template("machine/create.html")


@machine_blueprint.route("/enable-secure-boot", methods=["GET"])
@machine_blueprint.route("/<string:name_or_id>/enable-secure-boot", methods=["GET"])
@requires_session
@convert_id_to_model("machine")
def enable_secure_boot(machine: Machine) -> Response | str:
    """Endpoint to enable secure boot for a specified machine."""
    machine.configure_secure_boot()
    machine.secure_boot_state = True
    flash("Enabled secure boot.", "info")
    return redirect(url_for("machine.edit", id=machine.id))


@machine_blueprint.route("/disable-secure-boot", methods=["GET"])
@machine_blueprint.route("/<string:name_or_id>/disable-secure-boot", methods=["GET"])
@requires_session
@convert_id_to_model("machine")
def disable_secure_boot(machine: Machine) -> Response | str:
    """Endpoint to disable secure boot for a specified machine."""
    machine.secure_boot_state = False
    flash("Disabled secure boot.", "warning")
    return redirect(url_for("machine.edit", id=machine.id))


@machine_blueprint.route("/logs", methods=["GET"])
@machine_blueprint.route("/<string:name_or_id>/logs", methods=["GET"])
@requires_session
@convert_id_to_model("machine")
def logs(machine: Machine) -> Response | str:
    """Endpoint to view logs for a specified machine."""
    try:
        index = int(request.args.get("index", 0))
        if index not in machine.log_indexes:
            raise ValueError("Log index does not exist")
    except ValueError:
        abort(400, "Invalid log index.")
    return render_template("machine/logs.html", machine=machine, index=index)
