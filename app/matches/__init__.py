from flask import Blueprint

matches = Blueprint('matches', __name__)

from . import routes

