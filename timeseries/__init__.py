from flask import Blueprint
timeseries = Blueprint('timeseries', __name__)

# import routes
from . import routes