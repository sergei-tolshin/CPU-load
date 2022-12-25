from http import HTTPStatus

from flasgger import SwaggerView, swag_from
from flask import jsonify, request
from flask_babel import _
from marshmallow import ValidationError
from sqlalchemy import func

from src.app import db
from src.app.core.errors import error_response
from src.app.models.client import Client, CPULoad
from src.app.schemas.client import ClientCPULoadSchema, ClientSchema, CPULoadSchema


class ClientsAPI(SwaggerView):
    @swag_from('docs/clients_no_client_id_get.yml',
               endpoint='api.v1.clients.without_client_id')
    @swag_from('docs/clients_with_client_id_get.yml',
               endpoint='api.v1.clients.with_client_id')
    def get(self, client_id):
        """Информация о клиентах/клиенте"""
        if client_id is None:
            schema = ClientSchema(only=('id', 'name'), many=True)
            clients = Client.all()
            return jsonify(schema.dump(clients)), HTTPStatus.OK
        else:
            schema = ClientSchema()
            client = Client.query.get_or_404(client_id, _('Client not found'))
            return jsonify(schema.dump(client)), HTTPStatus.OK


class ClientCPULoadsAPI(SwaggerView):
    tags = ['clients']

    @swag_from('docs/clients_cpu_loads_get.yml')
    def get(self, client_id):
        """Информация о загрузках CPU клиента"""
        schema = CPULoadSchema(many=True)
        client = Client.query.get_or_404(client_id, _('Client not found'))

        cpu_loads = CPULoad.query.filter(
            CPULoad.client_id == client.id).order_by(CPULoad.created.desc())

        subq_cpu_loads_all = cpu_loads.subquery()
        subq_cpu_loads_last_100 = cpu_loads.limit(100).subquery()

        q_cpu_loads_all_aggr = db.select(
            func.min(subq_cpu_loads_all.c.load).label('min'),
            func.max(subq_cpu_loads_all.c.load).label('max'),
            func.avg(subq_cpu_loads_all.c.load).label('avg')
        )

        q_cpu_loads_last_100_aggr = db.select(
            func.min(subq_cpu_loads_last_100.c.load).label('min'),
            func.max(subq_cpu_loads_last_100.c.load).label('max'),
            func.avg(subq_cpu_loads_last_100.c.load).label('avg')
        )

        cpu_loads_all_aggr = db.session.execute(
            q_cpu_loads_all_aggr).first()
        cpu_loads_last_100_aggr = db.session.execute(
            q_cpu_loads_last_100_aggr).first()

        data = {
            'cpu_loads': schema.dump(cpu_loads.limit(100)),
            'all_aggr': {
                'min': cpu_loads_all_aggr.min,
                'max': cpu_loads_all_aggr.max,
                'avg': float('{:.1f}'.format(cpu_loads_all_aggr.avg))
            },
            'last_100_aggr': {
                'min': cpu_loads_last_100_aggr.min,
                'max': cpu_loads_last_100_aggr.max,
                'avg': float('{:.1f}'.format(cpu_loads_last_100_aggr.avg))
            },
        }

        return jsonify(data), HTTPStatus.OK

    @swag_from('docs/clients_cpu_load_post.yml')
    def post(self):
        """Получение от клиента информации о загрузке CPU в %"""
        schema = ClientCPULoadSchema()
        data = request.get_json()

        try:
            data = schema.load(data)
        except ValidationError as err:
            return error_response(HTTPStatus.UNPROCESSABLE_ENTITY,
                                  err.messages)

        client = Client.find_by_name(data.get('name'))
        if not client:
            client = Client(name=data.get('name'), ip=data.get('ip'))
            client = client.save()

        cpu_load = CPULoad(
            client_id=client.id,
            load=data.get('load')
        )
        cpu_load = cpu_load.save()

        return jsonify(id=cpu_load.id), HTTPStatus.CREATED
