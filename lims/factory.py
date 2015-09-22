# -*- coding: utf-8 -*-
from flask import Flask

from .api import api_bp
from .extensions import lims
from .settings import BaseConfig


def create_app(config=None, config_obj=None):
    app = Flask(__name__)
    app.config.from_object(config_obj or BaseConfig)
    if config is not None:
        app.config.from_pyfile(config)
    lims.init_app(app)
    app.register_blueprint(api_bp)
    return app
