from flask import render_template
from flask.views import MethodView
from flask_babel import _

from src.app.models.client import Client


class IndexView(MethodView):
    def get(self):
        return render_template('client/index.html')


class ClientView(MethodView):
    def get(self, client_id):
        context = {}

        if client_id is None:
            clients = Client.all()
            context['clients'] = clients
            return render_template('client/clients.html', context=context)
        else:
            client = Client.query.get_or_404(client_id, _('Client not found'))
            context['client'] = client
            return render_template('client/cpu_loads.html', context=context)
