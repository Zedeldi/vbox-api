"""Web interface for VirtualBox API."""

from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

from vbox_api import SOAPInterface, VBoxAPI

app = Flask(__name__)
interface = SOAPInterface()
interface.connect()
api = VBoxAPI(interface)


@app.errorhandler(HTTPException)
def handle_exception(error: HTTPException) -> str:
    """Handle HTTP errors."""
    return render_template("error.html", error=error), error.code


@app.route("/", methods=["GET"])
def dashboard() -> str:
    """Endpoint for dashboard."""
    return render_template("dashboard.html", machines=api.machines)
