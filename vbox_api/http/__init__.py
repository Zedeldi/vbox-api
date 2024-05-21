"""Web interface for VirtualBox API."""

from flask import Flask, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers.response import Response

from vbox_api.http import config
from vbox_api.http.session import SessionManager, requires_session
from vbox_api.http.views import blueprints

app = Flask(__name__)
app.config.from_object(config)

for url_prefix, blueprint in blueprints.items():
    app.register_blueprint(blueprint, url_prefix=url_prefix)

session_manager = SessionManager()


@app.before_request
def load_session() -> None:
    """Initialise Flask global application context object."""
    g.session_manager = session_manager
    g.api = session_manager.api
    g.username = session_manager.username


@app.errorhandler(HTTPException)
def handle_exception(error: HTTPException) -> tuple[str, int]:
    """Handle HTTP errors."""
    return render_template("error.html", error=error), error.code


@app.route("/", methods=["GET"])
@requires_session
def dashboard() -> Response | str:
    """Endpoint for dashboard."""
    return render_template("dashboard.html", machines=g.api.machines)


@app.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
    """Endpoint to login to interface."""
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        if not session_manager.login(username, password):
            flash("Incorrect username or password.", "danger")
        else:
            args = dict(request.args)
            next_endpoint = args.pop("next", None)
            if not next_endpoint:
                return redirect(url_for("dashboard"))
            return redirect(url_for(next_endpoint, **args))
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout() -> Response:
    """Endpoint to log out current session."""
    session_manager.logout()
    return redirect(url_for("dashboard"))
