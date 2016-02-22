# -*- coding: utf-8 -*-
ANALYSIS_MAP = {'EXO': 'exomes', 'WGS': 'genomes', 'RML': 'unknown',
                'MWG': 'microbial', 'MET': 'microbial', '16S': 'microbial'}
PRIORITIES = ['standard', 'priority', 'express', 'acute']


def internal_id(lims_sample, udf_key='Clinical Genomics ID'):
    """Get the sample id used internally."""
    if udf_key in dict(lims_sample.udf.items()):
        return lims_sample.udf[udf_key]

    # return normal lims id
    return lims_sample.id


def transform_entry(lims_sample):
    """Transform LIMS sample to dict."""
    data = dict(lims_sample.udf.items())
    if 'Sequencing Analysis' in lims_sample.udf:
        try:
            app_tag = analysis_info(lims_sample)
            # millions of reads
            target_reads = app_tag.get('reads', app_tag.get('coverage'))
            ianalysis_type = ANALYSIS_MAP[app_tag['analysis']]
        except ValueError:
            app_tag = {}
            target_reads = None
            ianalysis_type = None
    else:
        app_tag = None
        target_reads = None
        ianalysis_type = None

    sample_prio = data.get('priority', 'standard').lower().encode('utf-8')
    convert_prio = {'rutin': 'standard', 'förtur': 'priority',
                    'prioriterad': 'priority', '0': 'standard',
                    '000189t': 'standard', '000196t': 'standard',
                    'normal': 'standard', '000188t': 'standard'}
    if sample_prio in convert_prio:
        sample_prio = convert_prio.get(sample_prio)

    return {
        'id': lims_sample.id,
        'name': lims_sample.name,
        'project_name': lims_sample.project.name,
        'date_received': lims_sample.date_received,
        'customer': data.get('customer'),
        'family_id': data.get('familyID'),
        'mother_name': data.get('motherID'),
        'father_name': data.get('fatherID'),
        'gene_lists': data['Gene List'].split(';') if 'Gene List' in data else None,
        'gender': data.get('Gender'),
        'status': data.get('Status'),
        'app_tag_raw': data.get('Sequencing Analysis'),
        'app_tag': app_tag,
        'target_reads': target_reads,
        'data_analysis': data.get('Data Analysis'),
        'analysis_type': ianalysis_type,
        'priority': sample_prio
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
    if len(app_tag) == 10:
        data = {'analysis': app_tag[:3], 'library': app_tag[3:6]}
        if app_tag[6] == 'K':
            data['reads'] = int(app_tag[7:]) * 1000
        elif app_tag[6] == 'R':
            data['reads'] = int(app_tag[7:]) * 1000000
        elif app_tag[6] == 'C':
            data['coverage'] = int(app_tag[7:])

    elif len(app_tag) == 9:
        data = {'analysis': app_tag[:3], 'library': app_tag[3:6],
                'reads': int(app_tag[6:]) * 1000000}

    elif len(app_tag) == 8:
        # EXOSX100, EXSTA100
        data = {'analysis': 'EXO', 'library': 'SXT',
                'reads': int(app_tag[5:]) * 1000000}

    elif len(app_tag) == 12:
        # EXSTATRIO100
        data = {'analysis': 'EXO', 'library': 'SXT', 'reads': 100000000}

    else:
        raise ValueError("unknown application tag: {}".format(app_tag))

    return data
