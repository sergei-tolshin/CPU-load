from sqlalchemy.dialects.sqlite import FLOAT
from sqlalchemy_utils import IPAddressType

from src.app import db
from src.app.models.types import GUID

from .base import Base


class Client(Base):
    __tablename__ = 'client'

    name = db.Column(db.String(100), unique=True, nullable=False)
    ip = db.Column(IPAddressType)
    cpu_loads = db.relationship('CPULoad', backref='client')

    def __repr__(self):
        return '<Client {}>'.format(self.name)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


class CPULoad(Base):
    __tablename__ = 'cpu_load'

    load = db.Column(FLOAT)
    client_id = db.Column(GUID(), db.ForeignKey('client.id'), nullable=False)

    def __repr__(self):
        return '<CPULoad {}>'.format(self.load)
