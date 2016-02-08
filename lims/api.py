# -*- coding: utf-8 -*-
import logging

from genologics.entities import Sample
from genologics.lims import Lims
from requests.exceptions import HTTPError

from lims.exc import MissingLimsDataException
from lims.utils import transform_entry

logger = logging.getLogger(__name__)


class LimsAPI(object):

    """docstring for LimsAPI"""

    def __init__(self, lims=None):
        super(LimsAPI, self).__init__()
        self.lims = lims

    def init_app(self, app):
        """Connect with credentials from Flask app config."""
        self.connect(**app.config['LIMS_CONFIG'])

    def connect(self, baseuri, username, password):
        """Connect to the LIMS instance."""
        self.lims = Lims(baseuri, username, password)

    def sample(self, lims_id):
        """Get a sample from the LIMS."""
        logger.debug('fetch sample from LIMS')
        sample_obj = Sample(self.lims, id=lims_id)

        try:
            sample_json = transform_entry(sample_obj)
        except KeyError as error:
            message = "missing UDF: {}".format(error.message)
            logger.warn(message)
            raise MissingLimsDataException(message)
        except HTTPError as error:
            logger.warn('unknown lims id')
            raise error

        return sample_json

    def samples(self, project_id=None, case=None, sample_ids=None, limit=20,
                **kwargs):
        if project_id:
            sample_objs = self.lims.get_samples(projectname=project_id)
        elif case:
            sample_objs = self.lims.get_samples(udf={'customer': case[0],
                                                     'familyID': case[1]})
        else:
            sample_objs = self.lims.get_samples(**kwargs)

        sample_dicts = []
        for index, sample in enumerate(sample_objs):
            if index < limit:
                sample_dicts.append(transform_entry(sample))
            else:
                break

        analysis_types = set(sample['analysis_type'] for sample in
                             sample_dicts)
        case_data = {
            'analysis_types': list(analysis_types),
            'samples': sample_dicts
        }
        return case_data

    def cases(self):
        """Return a list of cases from the database."""
        samples = ((sample.udf['customer'], sample.udf['familyID'])
                   for sample in self.lims.get_samples()
                   if 'familyID' in sample.udf and 'customer' in sample.udf)
        return samples
