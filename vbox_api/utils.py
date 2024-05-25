"""Collection of miscellaneous functions to use within project."""

import base64
import re
import socket
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


def get_hostname() -> str:
    """Return hostname of local system."""
    return socket.gethostname()


def get_fqdn(name: Optional[str] = None) -> str:
    """Return fully-qualified domain name of host or hostname if not specified."""
    name = name or get_hostname()
    return socket.getfqdn(name)


def get_host_ip(name: Optional[str] = None) -> str:
    """Return host IP from name or hostname if not specified."""
    name = name or get_hostname()
    return socket.gethostbyname(name)


def get_available_port(host: str = "127.0.0.1") -> int:
    """
    Return available port number by binding to port 0.

    Please note that this function is subject to race conditions.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, 0))
        return sock.getsockname()[1]


def get_date_identifier(format_: str = "%Y-%m-%d_%H-%M-%S-%f") -> str:
    """Return date in the format of a string to be used as an identifier."""
    return datetime.now().strftime(format_)


def append_file_extension(path: str | Path, extension: str) -> Path:
    """Append extension to path if path does not already have a suffix."""
    path = Path(path)
    if path.suffix:
        return path
    return path.with_suffix(f".{extension}")


def image_to_data_uri(image: Image.Image) -> str:
    """Return data URI of image."""
    buffer = BytesIO()
    image_format = image.format if image.format else "PNG"
    image.save(buffer, format=image_format)
    image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/{image_format};base64,{image_b64}"


def text_to_image(
    text: str,
    size: tuple[int, int] = (800, 600),
    bg_colour: str = "black",
    font: ImageFont.ImageFont | ImageFont.FreeTypeFont = ImageFont.load_default(48),
    font_colour: str = "white",
) -> Image.Image:
    """Return image with specified text."""
    width, height = size
    image = Image.new("RGB", size, bg_colour)
    draw = ImageDraw.Draw(image)
    _, _, bbox_width, bbox_height = draw.textbbox((0, 0), text, font=font)
    draw.text(
        ((width - bbox_width) / 2, (height - bbox_height) / 2),
        text,
        font=font,
        fill=font_colour,
    )
    return image


def split_pascal_case(text: str, separator: str = " ") -> str:
    """Split PascalCase string and join with spaces."""
    return separator.join(
        re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", text)).split()
    )
