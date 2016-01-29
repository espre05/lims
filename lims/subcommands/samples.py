# -*- coding: utf-8 -*-
import json
import logging

import click

logger = logging.getLogger(__name__)


@click.command()
@click.option('-p', '--project', help='ticket or project id')
@click.option('-c', '--case', nargs=2, help='customer and case/family id')
@click.pass_context
def samples(context, project, case):
    """List samples in the database."""
    api = context.obj['api']
    try:
        case_data = api.samples(project_id=project, case=case)
    except ValueError as error:
        logger.warn(error.message)
        context.abort()

    click.echo(json.dumps(case_data, indent=4, sort_keys=True))
