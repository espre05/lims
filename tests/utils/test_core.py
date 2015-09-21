# -*- coding: utf-8 -*-
from lims.utils.core import (internal_id, transform_entry, analysis_type,
                             analysis_info, parse_application_tag)


def test_internal_id(lims):
    sample1 = lims['samples'][0]
    # test normal sample with lims id
    assert internal_id(sample1) == sample1.id

    # test sample with custom id
    sample1.udf['Clinical Genomics ID'] = 'custom_sample_id'
    assert internal_id(sample1) == 'custom_sample_id'


def test_transform_entry(lims):
    sample1 = lims['samples'][0]
    data = transform_entry(sample1)
    assert data['id'] == sample1.id
    assert data['gene_lists'] == ['IEM', 'EP']


def test_analysis_type(lims):
    sample1 = lims['samples'][0]
    assert analysis_type(sample1) == 'exomes'


def test_analysis_info(lims):
    sample1 = lims['samples'][0]
    data = analysis_info(sample1)
    assert data['reads'] == 100
    assert data['library'] == 'SXT'


def test_parse_application_tag():
    xt = 'EXOSXTR100'
    assert parse_application_tag(xt) == {'reads': 100, 'library': 'SXT',
                                         'analysis': 'EXO'}

    old_xt = 'EXSTA100'
    data = parse_application_tag(old_xt)
    assert data == {'reads': 100, 'library': 'SXT', 'analysis': 'EXO'}
