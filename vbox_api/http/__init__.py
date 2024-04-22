"""Web interface for VirtualBox API."""

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException

from vbox_api.http import config
from vbox_api.http.session import SessionManager

app = Flask(__name__)
app.config.from_object(config)
session_manager = SessionManager()


@app.errorhandler(HTTPException)
def handle_exception(error: HTTPException) -> str:
    """Handle HTTP errors."""
    return render_template("error.html", error=error), error.code


@app.route("/", methods=["GET"])
def dashboard() -> str:
    """Endpoint for dashboard."""
    if not session_manager.api:
        return redirect(url_for("login"))
    return render_template("dashboard.html", machines=session_manager.api.machines)


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    """Endpoint to login to interface."""
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        if not session_manager.login(username, password):
            flash("Incorrect username or password.", "danger")
        else:
            return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout() -> str:
    session_manager.logout()
    return redirect(url_for("dashboard"))
