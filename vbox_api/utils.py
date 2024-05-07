import base64
import re
import socket
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


def get_available_port(host: str = "127.0.0.1") -> int:
    """
    Return available port number by binding to port 0.

    Please note that this function is subject to race conditions.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, 0))
        return sock.getsockname()[1]


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


def split_pascal_case(text: str) -> str:
    """Split PascalCase string and join with spaces."""
    return " ".join(re.findall("([A-Z]+[^A-Z]+)", text)) or text
