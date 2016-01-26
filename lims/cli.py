# -*- coding: utf-8 -*-
import logging

import click
from genologics.lims import Lims
import yaml

from .subcommands import pedigree_cmd, sample_cmd, samples_cmd

logger = logging.getLogger()


@click.group()
@click.option('-c', '--config', type=click.File('r'))
@click.pass_context
def root(context, config):
    """Root command for CLI."""
    logger.addHandler(logging.StreamHandler())
    conf = yaml.load(config)
    context.obj = {'lims': Lims(**conf['lims'])}

root.add_command(sample_cmd)
root.add_command(samples_cmd)
root.add_command(pedigree_cmd)
