import argparse

from src.app import create_app, db
from src.app.models.client import Client, CPULoad

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Client': Client, 'CPULoad': CPULoad}


def run_server():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host')
    parser.add_argument('--port')
    args = parser.parse_args()
    host = args.host if args.host else '127.0.0.1'
    port = args.port if args.port else '5000'
    app.run(host=host, port=port)

