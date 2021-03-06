from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from config import config


bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)

    from .matches import matches as matches_blueprint
    app.register_blueprint(matches_blueprint, url_prefix='/matches')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

