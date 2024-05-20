"""Collection of useful functions for HTTP interface."""

import functools
from typing import Any, Callable, Optional

from flask import abort, g, request

from vbox_api.models.base import BaseModel


def get_model_from_name_or_id(
    model_name: str, name_or_id: Optional[str] = None, url_parameter: str = "id"
) -> BaseModel:
    """Return model instance from name_or_id for model_name or abort request."""
    name_or_id = name_or_id or request.args.get(url_parameter)
    if not name_or_id:
        abort(400, f"No {model_name.lower()} specified.")
    model = g.api.find_model(model_name, name_or_id)
    if not model:
        abort(400, f"Cannot find specified {model_name.lower()}.")
    return model


def convert_id_to_model(model_name: str, url_parameter: str = "id") -> Callable:
    """Decorate a function to convert model ID or name to object."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def inner(name_or_id: Optional[str] = None, *args, **kwargs) -> Any:
            model = get_model_from_name_or_id(model_name, name_or_id, url_parameter)
            return func(model, *args, **kwargs)

        return inner

    return decorator
