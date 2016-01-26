# -*- coding: utf-8 -*-
import json
import logging

import click

from lims.utils import transform_entry

logger = logging.getLogger(__name__)


@click.command()
@click.option('-p', '--project', help='ticket or project id')
@click.option('-c', '--case', nargs=2, help='customer and case/family id')
@click.pass_context
def samples(context, project, case):
    """List samples in the database."""
    lims = context.obj['lims']
    if project:
        sample_objs = lims.get_samples(projectname=project)
    elif case:
        sample_objs = lims.get_samples(udf={'customer': case[0],
                                            'familyID': case[1]})
    else:
        logger.warn('provide either project or cust/case ids')
        context.abort()
    sample_dicts = [transform_entry(sample) for sample in sample_objs]
    analysis_types = set(sample['analysis_type'] for sample in
                         sample_dicts)
    case_data = {
        'analysis_types': list(analysis_types),
        'samples': sample_dicts
    }

    click.echo(json.dumps(case_data, indent=4, sort_keys=True))
