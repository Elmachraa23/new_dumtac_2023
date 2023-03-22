# eventlet for deployment
#import eventlet
#eventlet.monkey_patch()

from importlib import import_module
from logging import getLogger, Formatter, INFO
from logging.handlers import TimedRotatingFileHandler

from flask import Flask

from flask_cors import CORS
from flask_login import LoginManager

from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import CSRFProtect

import app

from flask_apscheduler import APScheduler
from flask_babel import Babel
from flask_moment import Moment

documents = UploadSet('documents', ('jpg','jpe','jpeg','png','pdf'))
images = UploadSet('images', IMAGES)
pictures = UploadSet('pictures', IMAGES)

cors = CORS()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
socket = SocketIO(cors_allowed_origins='*')
scheduler = APScheduler()
babel = Babel()
moment = Moment()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

    cors.init_app(app)
    csrf.init_app(app)
    socket.init_app(app)

    babel.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    for module_name in ('base', 'admin', 'site'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def configure_logs(app):
    try:
        logger = getLogger()

        rotationHandler = TimedRotatingFileHandler(filename='logs/runtime.log', utc=True, when='W0', backupCount=15, encoding='utf-8', delay=True)
        formatter = Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        rotationHandler.setFormatter(formatter)
        #rotationHandler.setLevel(INFO)

        logger.addHandler(rotationHandler)
        logger.setLevel(INFO)
        logger.info('Konco Dev Logger startup')
    except:
        pass


def init_scheduler(app):
    scheduler.init_app(app)
    scheduler.start()


def create_app(config, selenium=False):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)

    register_extensions(app)
    configure_database(app)
    configure_logs(app)
    configure_uploads(app, (documents, images, pictures))

    with app.app_context():
        register_blueprints(app)
        init_scheduler(app)

    return app
