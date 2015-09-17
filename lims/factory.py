# -*- coding: utf-8 -*-
from flask import Flask

from .api import api_bp
from .extensions import lims
from .settings import BaseConfig


def create_app(config_obj=None):
    app = Flask(__name__)
    app.config.from_object(config_obj or BaseConfig)
    lims.init_app(app)
    app.register_blueprint(api_bp)
    return app
