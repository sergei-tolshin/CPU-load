from flask import Blueprint

from src.app.api.v1.urls import v1

api = Blueprint('api', __name__, url_prefix='/api')

api.register_blueprint(v1)
