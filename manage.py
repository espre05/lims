#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.script import Manager, Server

from lims.factory import create_app
from lims.settings import DevConfig

app = create_app(config_obj=DevConfig)
manager = Manager(app)


manager.add_command('vagrant', Server(host='0.0.0.0', use_reloader=True))


if __name__ == '__main__':
    manager.run()
