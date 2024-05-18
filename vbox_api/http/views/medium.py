"""Blueprint for medium endpoints."""

from flask import Blueprint, g, render_template
from werkzeug.wrappers.response import Response

from vbox_api.http.session import requires_session

medium_blueprint = Blueprint("medium", __name__)


@medium_blueprint.route("/", methods=["GET"])
@requires_session
def view() -> Response | str:
    """Endpoint to view all mediums."""
    return render_template("medium/view.html", api=g.api)
