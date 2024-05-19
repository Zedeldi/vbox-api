"""Blueprint for medium endpoints."""

from flask import Blueprint, g, render_template, send_file
from werkzeug.wrappers.response import Response

from vbox_api.models import Medium
from vbox_api.http.session import requires_session
from vbox_api.http.utils import convert_id_to_model

medium_blueprint = Blueprint("medium", __name__)


@medium_blueprint.route("/", methods=["GET"])
@requires_session
def view() -> Response | str:
    """Endpoint to view all mediums."""
    return render_template("medium/view.html")


@medium_blueprint.route("/download", methods=["GET"])
@medium_blueprint.route("/<string:name_or_id>/download", methods=["GET"])
@requires_session
@convert_id_to_model("medium")
def download(medium: Medium) -> Response | str:
    """Endpoint to download a medium."""
    return send_file(medium.path, as_attachment=True)
