# -*- coding: utf-8 -*-
import json
import logging

import click
from requests.exceptions import HTTPError

from lims.exc import MissingLimsDataException

logger = logging.getLogger(__name__)


@click.command()
@click.argument('lims_id')
@click.pass_context
def sample(context, lims_id):
    """Get information on samples."""
    api = context.obj['api']
    try:
        sample_json = api.sample(lims_id)
    except MissingLimsDataException as error:
        logger.warn(error.message)
        context.abort()
    except HTTPError as error:
        context.abort()

    click.echo(json.dumps(sample_json, indent=4, sort_keys=True))
