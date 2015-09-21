# -*- coding: utf-8 -*-
import codecs
import logging

from flask import abort, Blueprint, jsonify, request
from flask.ext.restful import Api, Resource
from genologics.entities import Sample
from requests.exceptions import HTTPError

from .exc import LimsSampleNotFoundError, MissingLimsDataException
from .extensions import lims
from .utils import analysis_info, serialize_pedigree, transform_entry

logger = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


@api_bp.route('/samples/<lims_id>')
def sample(lims_id):
    """Get a sample from LIMS."""
    sample_obj = Sample(lims, id=lims_id)

    try:
        sample_json = transform_entry(sample_obj)
    except KeyError as error:
        return abort(400, "missing UDF: {}".format(error.message))
    except HTTPError as error:
        return abort(404, error.message)
    return jsonify(**sample_json)


@api_bp.route('/samples/validate/<lims_id>')
def validate_sample(lims_id):
    """Validate information in the LIMS on sample level."""
    logger.debug('fetch sample from LIMS')
    sample_obj = Sample(lims, id=lims_id)

    try:
        sample_obj.udf['familyID']
        sample_obj.udf['customer']
    except KeyError as error:
        raise MissingLimsDataException(error.message)
    except HTTPError as error:
        raise LimsSampleNotFoundError(error.message)
    return jsonify(passed=True)


@api_bp.route('/cases/pedigree/<cust_id>/<case_id>')
def pedigree(cust_id, case_id):
    """Generate pedigree content for a case."""
    out_path = request.args.get('target')
    ped_content = serialize_pedigree(lims, cust_id, case_id)

    if out_path:
        try:
            with codecs.open(out_path, 'w') as handle:
                handle.write(ped_content)
        except IOError:
            return abort(400, "Target path doesn't exist: {}".format(out_path))

    return jsonify(content=ped_content, location=out_path)


class SamplesApi(Resource):
    def get(self):
        """List samples in the database."""
        project_id = request.args.get('project_id')
        cust_id = request.args.get('cust_id')
        case_id = request.args.get('case_id')

        if project_id:
            sample_objs = lims.get_samples(projectname=project_id)
        elif cust_id and case_id:
            sample_objs = lims.get_samples(udf={'customer': cust_id,
                                                'familyID': case_id})
        else:
            return abort(400, 'provide either project or cust/case ids')
        sample_dicts = [transform_entry(sample) for sample in sample_objs]
        analysis_types = set(sample['analysis_type'] for sample in
                             sample_dicts)
        case_data = {
            'analysis_types': list(analysis_types),
            'samples': sample_dicts
        }
        return case_data


api.add_resource(SamplesApi, '/samples', endpoint='samples')
