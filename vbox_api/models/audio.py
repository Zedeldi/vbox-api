from vbox_api.models.base import BaseModel, ModelRegister


class AudioSettings(BaseModel, metaclass=ModelRegister):
    """Class to handle AudioSettings attributes and methods."""

    _PROPERTY_INTERFACE_ALIASES: dict[str, str] = {"Adapter": "IAudioAdapter"}
