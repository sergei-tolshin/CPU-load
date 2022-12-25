from flasgger import Swagger
from flask import Flask
from flask_babel import Babel
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.app.core.config import Config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
swagger = Swagger()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    swagger.init_app(app)
    babel.init_app(app)

    from src.app.api.urls import api
    from src.app.client.urls import client

    app.register_blueprint(api)
    app.register_blueprint(client)

    return app
