from marshmallow import fields

from src.app import ma
from src.app.models.client import Client, CPULoad


class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        fields = ('id', 'name', 'ip', 'created',)
        ordered = True
        load_instance = True


class CPULoadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CPULoad
        fields = ('id', 'load', 'created')
        ordered = True

    load = fields.Float()
    created = fields.DateTime(format='%d.%m.%Y %H:%M:%S%z')


class ClientCPULoadSchema(ma.Schema):
    name = fields.Str()
    ip = fields.IPv4()
    load = fields.Float()
