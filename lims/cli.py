# -*- coding: utf-8 -*-
from flask.ext.script import Manager

from .factory import create_app
from .settings import DevConfig

app = create_app(config_obj=DevConfig)
manager = Manager(app)


def main():
    """Start microservice."""
    manager.run()
