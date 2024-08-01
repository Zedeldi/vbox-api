"""Desktop GUI wrapper for Flask application."""

from flaskwebgui import FlaskUI

from vbox_api.http import app

ui = FlaskUI(app=app, server="flask")

if __name__ == "__main__":
    ui.run()
