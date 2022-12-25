from flask import Blueprint

core = Blueprint('core', __name__)

from src.app.core import errors
