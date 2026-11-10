from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from app.main import main


def create_app():
    app = Flask(__name__)

    PrometheusMetrics(app)
    app.register_blueprint(main)

    return app
