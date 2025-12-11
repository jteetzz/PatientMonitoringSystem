from flask import Blueprint

web_bp = Blueprint(
    "web",
    __name__,
    template_folder="templates",  # web/templates
    static_folder="static",       # web/static
)

from . import routes  # make sure routes register on web_bp

