#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from werkzeug.contrib.fixers import ProxyFix

from lims.factory import create_app

app = create_app(config=os.environ.get('FLASK_CONFIG'))
app.wsgi_app = ProxyFix(app.wsgi_app)


if __name__ == '__main__':
    app.run()
