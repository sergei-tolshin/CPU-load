from flask import Blueprint

from .views import ClientView, IndexView

client = Blueprint('clients', __name__, url_prefix='/')

client.add_url_rule('/',
                    view_func=IndexView.as_view('index'),
                    endpoint='index',
                    methods=['GET']
                    )

client.add_url_rule('/clients/',
                    defaults={'client_id': None},
                    view_func=ClientView.as_view('client_view'),
                    endpoint='without_client_id',
                    methods=['GET']
                    )

client.add_url_rule('/clients/<uuid:client_id>/',
                    view_func=ClientView.as_view('client_view'),
                    endpoint='with_client_id',
                    methods=['GET'])
