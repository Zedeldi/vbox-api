from vbox_api.http.views.machine import machine_blueprint
from vbox_api.http.views.medium import medium_blueprint

__all__ = ["machine_blueprint", "medium_blueprint"]

blueprints = {
    f"/{machine_blueprint.name}": machine_blueprint,
    f"/{medium_blueprint.name}": medium_blueprint,
}
