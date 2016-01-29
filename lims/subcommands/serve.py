# -*- coding: utf-8 -*-
import click

from lims.server import create_app


@click.command()
@click.option('--debug', is_flag=True)
@click.option('--port', default=5000)
@click.pass_context
def serve(context, debug, port):
    """Serve up a web interface."""
    app = create_app('lims', config_obj=context.obj)
    app.run(debug=debug, port=port)
