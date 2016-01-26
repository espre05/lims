# -*- coding: utf-8 -*-
import json
import logging

import click
from genologics.entities import Sample
from requests.exceptions import HTTPError

from lims.exc import MissingLimsDataException
from lims.utils import transform_entry

logger = logging.getLogger(__name__)


@click.command()
@click.option('--validate', is_flag=True)
@click.argument('lims_id')
@click.pass_context
def sample(context, validate, lims_id):
    """Get information on samples."""
    lims = context.obj['lims']
    logger.debug('fetch sample from LIMS')
    sample_obj = Sample(lims, id=lims_id)

    try:
        if validate:
            try:
                sample_obj.udf['familyID']
                sample_obj.udf['customer']
            except KeyError as error:
                raise MissingLimsDataException(error.message)

        try:
            sample_json = transform_entry(sample_obj)
        except KeyError as error:
            logger.warn("missing UDF: {}".format(error.message))
            context.abort()
    except HTTPError as error:
        logger.warn('unknown lims id')
        context.abort()

    click.echo(json.dumps(sample_json, indent=4, sort_keys=True))
