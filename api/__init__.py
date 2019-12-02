from flask import Blueprint
api = Blueprint('api', __name__)

# import routes
from . import routes