# -*- coding: utf-8 -*-
import logging

from flask import (abort, Blueprint, current_app as app, redirect,
                   render_template, request, url_for)
import requests

logger = logging.getLogger(__name__)
lims_bp = Blueprint('lims', __name__, template_folder='templates')


@lims_bp.route('/')
def index():
    """Display the overview page with search functions."""
    return render_template('index.html')


@lims_bp.route('/samples/<lims_id>')
def sample(lims_id):
    """Display details on a sample."""
    try:
        sample_obj = app.config['api'].sample(lims_id)
    except requests.HTTPError as error:
        logger.warn(error.message)
        return abort(404, error.message)
    return render_template('sample.html', sample=sample_obj)


@lims_bp.route('/samples', methods=['POST'])
def samples():
    """Search for samples."""
    lims_id = request.form['lims_id']
    if lims_id:
        return redirect(url_for('.sample', lims_id=lims_id))
    elif request.form['cust_id'] and request.form['case_id']:
        cust_id = request.form['cust_id']
        case_id = request.form['case_id']
        return redirect(url_for('.case', cust_id=cust_id, case_id=case_id))
    elif request.form['project_id']:
        return redirect(url_for('.project',
                                project_id=request.form['project_id']))
    else:
        return redirect(request.referrer)


@lims_bp.route('/cases/<cust_id>/<case_id>')
def case(cust_id, case_id):
    """Display information on a case with samples."""
    case_data = app.config['api'].samples(case=(cust_id, case_id))
    return render_template('case.html', cust_id=cust_id, case_id=case_id,
                           **case_data)


@lims_bp.route('/projects/<project_id>')
def project(project_id):
    """Display samples in a project."""
    sample_data = app.config['api'].samples(project_id=project_id)
    return render_template('project.html', project_id=project_id, **sample_data)
