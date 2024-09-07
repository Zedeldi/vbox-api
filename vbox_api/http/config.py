"""Configuration file for Flask application."""

import logging

from vbox_api.http.constants import UserPermission

SECRET_KEY = "development"
OPERATION_TIMEOUT_MS = 1000

LOG_FILE = "/tmp/vbox-api.log"
# Setting log level to logging.DEBUG will include handles
LOG_LEVEL = logging.INFO

USER_PERMISSIONS = UserPermission.START_VBOXWEBSRV | UserPermission.READ_EVENTS

DEFAULT_MEDIUM_SIZE = 32 * 1024 * 1024 * 1024

WEBSOCKET_PROXY_LISTEN_HOST = "0.0.0.0"
WEBSOCKET_PROXY_TIMEOUT = 60
WEBSOCKET_PROXY_VNC_PATH = "/usr/share/webapps/novnc"
