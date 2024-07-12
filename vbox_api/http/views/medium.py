"""Blueprint for medium endpoints."""

import logging
from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from werkzeug.utils import secure_filename
from werkzeug.wrappers.response import Response

from vbox_api import utils
from vbox_api.constants import AccessMode, MediumState
from vbox_api.http.session import requires_session
from vbox_api.http.utils import convert_id_to_model
from vbox_api.models import Medium

logger = logging.getLogger(__name__)
medium_blueprint = Blueprint("medium", __name__)


def get_new_medium_path(name: str | Path) -> Path:
    """Return secure file path for a new medium."""
    name = str(name)
    return (
        g.api.system_properties.default_machine_folder / Path(secure_filename(name))
    ).absolute()


def create_medium_from_upload() -> Medium | Response:
    """Create new medium from uploaded file."""
    device_type = request.form.get("device_type")
    file = request.files["file"]
    if not file or file.filename == "":
        flash("No selected file", "danger")
        return redirect(request.url)
    path = get_new_medium_path(file.filename)
    file.save(path)
    medium = g.api.open_medium(path, device_type, AccessMode.READ_WRITE, False)
    return medium


def create_medium_from_new() -> Medium:
    """Create new medium from form information."""
    size = int(request.form.get("size") or current_app.config["DEFAULT_MEDIUM_SIZE"])
    format_ = request.form.get("format")
    device_type = request.form.get("device_type")
    name = utils.append_file_extension(
        request.form.get("name") or utils.get_date_identifier(), format_.lower()
    )
    path = get_new_medium_path(name)
    medium = g.api.create_medium_with_defaults(
        path, size, format_, AccessMode.READ_WRITE, device_type
    )
    return medium


@medium_blueprint.route("/", methods=["GET"])
@requires_session
def overview() -> Response | str:
    """Endpoint to view all mediums."""
    return render_template("medium/overview.html")


@medium_blueprint.route("/create", methods=["GET", "POST"])
@requires_session
def create() -> Response | str:
    """Endpoint to create a new medium."""
    if request.method == "POST":
        if "file" in request.files:
            medium = create_medium_from_upload()
        else:
            medium = create_medium_from_new()
        if medium.state == MediumState.NOT_CREATED:
            flash("Could not create medium.", "danger")
            return redirect(request.url)
        return redirect(url_for("medium.overview"))
    return render_template("medium/create.html", utils=utils)


@medium_blueprint.route("/download", methods=["GET"])
@medium_blueprint.route("/<string:name_or_id>/download", methods=["GET"])
@requires_session
@convert_id_to_model("medium")
def download(medium: Medium) -> Response | str:
    """Endpoint to download a medium."""
    return send_file(medium.path, as_attachment=True)


@medium_blueprint.route("/delete", methods=["GET"])
@medium_blueprint.route("/<string:name_or_id>/delete", methods=["GET"])
@requires_session
@convert_id_to_model("medium")
def delete(medium: Medium) -> Response | str:
    """Endpoint to delete a medium."""
    logger.warning(f"Deleting medium '{medium.name}'")
    progress = medium.delete_storage()
    flash("Deleting medium...", "warning")
    progress.wait_for_completion(current_app.config["OPERATION_TIMEOUT_MS"])
    return redirect(url_for("medium.overview"))
