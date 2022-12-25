import uuid
from datetime import datetime

from src.app import db
from src.app.models.types import GUID

from .mixins import BaseMixin


class Base(db.Model, BaseMixin):
    __abstract__ = True

    id = db.Column(GUID(), primary_key=True, default=lambda: str(
        uuid.uuid4()), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
