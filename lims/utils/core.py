# -*- coding: utf-8 -*-
ANALYSIS_MAP = {'EXO': 'exomes', 'WGS': 'genomes'}


def internal_id(lims_sample, udf_key='Clinical Genomics ID'):
    """Get the sample id used internally."""
    if udf_key in dict(lims_sample.udf.items()):
        return lims_sample.udf[udf_key]

    # return normal lims id
    return lims_sample.id


def transform_entry(lims_sample):
    """Transform LIMS sample to dict."""
    data = dict(lims_sample.udf.items())
    app_tag = analysis_info(lims_sample)
    # millions of reads
    target_reads = app_tag['reads'] * 1000000

    return {
        'id': lims_sample.id,
        'name': lims_sample.name,
        'project_name': lims_sample.project.name,
        'date_received': lims_sample.date_received,
        'customer': data['customer'],
        'family_id': data['familyID'],
        'mother_name': data.get('motherID'),
        'father_name': data.get('fatherID'),
        'gene_lists': data['Gene List'].split(';'),
        'gender': data['Gender'],
        'status': data['Status'],
        'app_tag_raw': data['Sequencing Analysis'],
        'app_tag': app_tag,
        'target_reads': target_reads,
        'data_analysis': data['Data Analysis'],
        'analysis_type': ANALYSIS_MAP[app_tag['analysis']]
    }


def collect_case(lims, cust_id, case_id):
    """Fetch all samples for a case from the LIMS."""
    samples = lims.get_samples(udf={'customer': cust_id, 'familyID': case_id})
    return samples


def analysis_type(lims_sample):
    app_tag = analysis_info(lims_sample)
    return ANALYSIS_MAP[app_tag['analysis']]


def analysis_info(lims_sample):
    """Figure out type of sequencing for a sample."""
    app_tag = lims_sample.udf['Sequencing Analysis']
    info = parse_application_tag(app_tag)
    return info


def parse_application_tag(app_tag):
    """Parse out the components of the application tag."""
    if len(app_tag) == 8:
        data = {'analysis': 'EXO', 'library': 'SXT', 'reads': int(app_tag[5:])}
    elif len(app_tag) == 10:
        data = {'analysis': app_tag[:3], 'library': app_tag[3:6],
                'reads': int(app_tag[7:10])}
    return data
