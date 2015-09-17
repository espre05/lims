# -*- coding: utf-8 -*-
import pytest

from lims.factory import create_app
from lims.settings import TestConfig


@pytest.fixture
def app(request):
    app = create_app(config_obj=TestConfig)
    return app


@pytest.fixture(scope='function')
def lims():
    return {
        'samples': add_samples()
    }


class LimsSample(object):
    def __init__(self, lims_id, name, date_recieved, project_id, **udfs):
        self.id = lims_id
        self.name = name
        self.date_recieved = date_recieved
        self.udf = udfs
        self.project = LimsProject(project_id)


class LimsProject(object):
    def __init__(self, name):
        self.name = name


def add_samples():
    """Add some fake samples mimicing LIMS samples."""
    samples = [LimsSample('ADM1003A5', '15045-I-1A', '2015-04-24', '517832',
                          customer='cust003', familyID='15045',
                          motherID='15045-II-2U', fatherID='15045-II-1U',
                          Gender='man', Status='affected',
                          **{'Gene List': 'IEM,EP',
                             'Sequencing Analysis': 'EXOSXTR100',
                             'Data Analysis': 'scout'}),
               LimsSample('ADM1003A5', '15101-II-2U', '2015-03-13', '375994',
                          customer='cust003', familyID='15101',
                          motherID='0', fatherID='0',
                          Gender='F', Status='Unaffected',
                          **{'Gene List': 'EP',
                             'Sequencing Analysis': 'EXOSXTR100',
                             'Data Analysis': 'scout'})]

    return samples
