# -*- coding: utf-8 -*-
"""
Module to provide utilities for creating and managing pedigree files
in the ``.ped`` format. Uses the excellent "ped-parser" package by
Måns Mangnusson.

Provides utilities for transforming output from the LIMS/order form
to a more or less standard ``.ped`` file format.
"""
import logging

from lims.exc import LimsCaseIdNotFoundError
from .core import analysis_type, collect_case, internal_id

MANDATORY_HEADERS = ('Family ID', 'Individual ID', 'Paternal ID',
                     'Maternal ID', 'Sex', 'Phenotype')
WES_ONLY_HEADERS = ('Capture_kit',)
SCOUT_HEADERS = ('Clinical_db', 'display_name', 'Sequencing_type')
WES_HEADERS = MANDATORY_HEADERS + WES_ONLY_HEADERS + SCOUT_HEADERS
WGS_HEADERS = MANDATORY_HEADERS + SCOUT_HEADERS
CAPTUREKIT_MAP = {'Agilent Sureselect CRE': 'Agilent_SureSelectCRE.V1',
                  'Agilent Sureselect V5': 'Agilent_SureSelect.V5'}


logger = logging.getLogger(__name__)


def serialize_pedigree(lims, cust_id, case_id):
    """Write a pedigree file from data in the LIMS."""
    logger.debug("collecting samples from case: %s", case_id)
    samples = collect_case(lims, cust_id, case_id)
    if len(samples) == 0:
        raise LimsCaseIdNotFoundError(case_id)
    sample_dict = {sample.name: internal_id(sample) for sample in samples}

    logger.debug('extract data from LIMS samples')
    ped_data = [transform_entry(lims, sample, id_dict=sample_dict)
                for sample in samples]

    capture_kits = set(data.get('Capture_kit') for data in ped_data)
    headers = WES_HEADERS
    if len(capture_kits) == 1:
        logger.debug('all samples use the sample or no capture kit')
        if None in capture_kits:
            logger.debug('all samples are WGS')
            headers = WGS_HEADERS
    else:
        if None in capture_kits:
            logger.debug('case is a mix, unify capture kit')
            # get the first item which isn't ``None`` from a list
            capture_kit = next(item for item in capture_kits
                               if item is not None)
            # fill in a fake capture kit for the WGS samples
            for data in ped_data:
                if 'Capture_kit' not in data:
                    data['Capture_kit'] = capture_kit
        else:
            logger.debug('samples use different capture kits')

    logger.debug('serialize sample data to ped format')
    ped_lines = serialize_samples(ped_data, headers=headers)
    ped_content = '\n'.join(ped_lines)
    return ped_content


def get_capturekit(lims, lims_sample, udf_key='Capture Library version',
                   udf_kitkey='Capture Library version'):
    """Figure out which capture kit has been used for the sample."""
    hybrizelib_id = '33'
    if udf_key in dict(lims_sample.udf.items()):
        logger.debug('prefer capture kit annotated on the sample level')
        capture_kit = lims_sample.udf[udf_key]
    else:
        artifacts = lims.get_artifacts(samplelimsid=lims_sample.id,
                                       type='Analyte')
        capture_kit = None
        for artifact in artifacts:
            if artifact.parent_process:
                if artifact.parent_process.type.id == hybrizelib_id:
                    try:
                        capture_kit = artifact.parent_process.udf[udf_kitkey]
                    except KeyError:
                        logger.warn('capture kit not found on expected process')
                        continue
                    break

        # return the MIP capture kit id
        if capture_kit is None:
            raise AttributeError('No capture kit annotated')

    return CAPTUREKIT_MAP[capture_kit.strip()]


def transform_entry(lims, sample, id_dict):
    """Extract relevant data from a LIMS sample entry."""
    udfs = dict(sample.udf.items())
    gender = udfs['Gender']
    sex = {'M': 1, 'F': 2}.get(gender, 'other')
    status = udfs['Status']
    phenotype = {'Unaffected': 1, 'Affected': 2}.get(status, 0)

    father_lims_id = id_dict.get(udfs.get('fatherID'), '0')
    mother_lims_id = id_dict.get(udfs.get('motherID'), '0')

    data = {
        'Family ID': udfs['familyID'],
        'Individual ID': internal_id(sample),
        'Paternal ID': father_lims_id,
        'Maternal ID': mother_lims_id,
        'Sex': sex,
        'Phenotype': phenotype,
        'Clinical_db': udfs.get('Gene List', '').split(';'),
        'display_name': sample.name
    }

    analysis_tag = analysis_type(sample)
    if analysis_tag == 'exomes':
        logger.debug('run as WES, expect capture kit')
        data['Capture_kit'] = get_capturekit(lims, sample)
        data['Sequencing_type'] = 'WES'
    elif analysis_tag == 'genomes':
        logger.debug('run as WGS, skip capture kit')
        data['Sequencing_type'] = 'WGS'
    else:
        raise AttributeError('unexpected application tag')

    return data


def serialize_samples(data_list, headers=WES_HEADERS):
    """Serialize a sample in the ``.ped`` format."""
    # serialize the header
    yield '#' + '\t'.join(headers)

    # serialize the samples
    for data in data_list:
        row = (';'.join(data.get(key, [])) if isinstance(data.get(key), list)
               else str(data.get(key, '')) for key in headers)
        yield '\t'.join(row)
