"""Desktop GUI wrapper for Flask application."""

from flaskwebgui import FlaskUI

from vbox_api.http import app

ui = FlaskUI(
    app=app, server="flask", extra_flags=["--guest"], profile_dir_prefix="vbox_api-"
)


def main() -> None:
    """Start FlaskUI desktop GUI application."""
    ui.run()


if __name__ == "__main__":
    main()
