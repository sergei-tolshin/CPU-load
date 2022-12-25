from flask import Blueprint

from .views import ClientCPULoadsAPI, ClientsAPI

router = Blueprint('clients', __name__, url_prefix='/clients')

clients_view = ClientsAPI.as_view('client_api')

router.add_url_rule('/',
                    defaults={'client_id': None},
                    view_func=clients_view,
                    endpoint='without_client_id',
                    methods=['GET'])

router.add_url_rule('/cpu_load/',
                    view_func=ClientCPULoadsAPI.as_view('cpu_load'),
                    methods=['POST'])

router.add_url_rule('/<uuid:client_id>',
                    view_func=clients_view,
                    endpoint='with_client_id',
                    methods=['GET'])

router.add_url_rule('/<uuid:client_id>/cpu_loads/',
                    view_func=ClientCPULoadsAPI.as_view('cpu_loads'),
                    methods=['GET'])
