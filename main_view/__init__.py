from flask import Blueprint
main_view = Blueprint('main_view', __name__)

# import routes
from . import routes