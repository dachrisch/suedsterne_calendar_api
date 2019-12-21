import logging.config
import os

from flask import Flask, Blueprint
from flask_dance.contrib.google import make_google_blueprint

import settings
from api.endpoints.deployment import ns as deployments_namespace
from api.restplus import api

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), './logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def create_app():
    flask_app = Flask(__name__)

    configure_app(flask_app)

    blueprint = make_google_blueprint(
        client_id=os.getenv('CLIENT_ID', 'client_id'),
        client_secret=os.getenv('CLIENT_SECRET', 'client_secret'),
    )
    flask_app.register_blueprint(blueprint, url_prefix="/login")

    blueprint = Blueprint('api', __name__, url_prefix='/api')

    api.init_app(blueprint)
    api.add_namespace(deployments_namespace)
    flask_app.register_blueprint(blueprint)

    return flask_app


def main():
    app = create_app()
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
