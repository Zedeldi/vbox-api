"""Configuration file for Flask application."""

SECRET_KEY = "development"
OPERATION_TIMEOUT_MS = 1000

DEFAULT_MEDIUM_SIZE = 32 * 1024 * 1024 * 1024

WEBSOCKET_PROXY_LISTEN_HOST = "0.0.0.0"
WEBSOCKET_PROXY_TIMEOUT = 60
WEBSOCKET_PROXY_VNC_PATH = "/usr/share/webapps/novnc"
