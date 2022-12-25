from flask import Blueprint

from .client.urls import router as client_router

v1 = Blueprint('v1', __name__, url_prefix='/v1')

v1.register_blueprint(client_router)
