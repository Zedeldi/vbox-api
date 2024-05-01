from vbox_api.models.base import BaseModel, ModelRegister


@BaseModel.register_model
class Progress(BaseModel, metaclass=ModelRegister):
    """Class to handle Progress attributes and methods."""
