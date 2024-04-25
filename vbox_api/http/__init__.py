"""Web interface for VirtualBox API."""

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers.response import Response

from vbox_api.http import config
from vbox_api.http.session import SessionManager, requires_session

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
