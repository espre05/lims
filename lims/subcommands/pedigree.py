# -*- coding: utf-8 -*-
import logging

import click

from lims.exc import LimsCaseIdNotFoundError
from lims.utils import serialize_pedigree

logger = logging.getLogger(__name__)


@click.command()
@click.option('-o', '--output', type=click.File('w'), default='-')
@click.argument('cust_id')
@click.argument('case_id')
@click.pass_context
def pedigree(context, output, cust_id, case_id):
    """Generate pedigree content for a case."""
    lims = context.obj['lims']
    try:
        ped_content = serialize_pedigree(lims, cust_id, case_id)
    except LimsCaseIdNotFoundError:
        logger.warn("missing case id: %s", case_id)
        context.abort()
    except AttributeError as error:
        logger.warn(error.message)
        context.abort()
    except KeyError as error:
        logger.warn("missing sample data: %s", error.message)
        context.abort()

    click.echo(ped_content, file=output)
