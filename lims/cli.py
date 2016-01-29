# -*- coding: utf-8 -*-
import logging

import click
from genologics.lims import Lims
import yaml

from .api import LimsAPI
from .subcommands import pedigree_cmd, sample_cmd, samples_cmd, serve_cmd

logger = logging.getLogger()


@click.group()
@click.option('-c', '--config', type=click.File('r'), required=True)
@click.pass_context
def root(context, config):
    """Root command for CLI."""
    logger.addHandler(logging.StreamHandler())
    conf = yaml.load(config)
    lims = Lims(**conf['lims'])
    context.obj = {'lims': lims, 'api': LimsAPI(lims)}


root.add_command(sample_cmd)
root.add_command(samples_cmd)
root.add_command(pedigree_cmd)
root.add_command(serve_cmd)
