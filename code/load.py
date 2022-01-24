# Load different data files for project
import re
import glob
import numpy as np
import pandas as pd


def load_data(type: str = 'farmers',
              **kwargs):
    '''
    Load complete data for either farmers or welders

    Returns
    ----------
    dat: pd.DataFrame
        Data frame with complete data
    '''

    # READ DATA #
    ids = pd.read_csv('../data/project_IDs.csv')
    ids = update_visit_info(ids)
    metabolites = pd.read_csv('../data/metabolite_concentration.csv')

    if type == 'farmers':
        full_project = _load_farmers()
    elif type == 'welders':
        full_project = _load_welders(**kwargs)
    else:
        raise ValueError('type should be farmers or welders')

    # MERGE DATA
    merge_left = ['project_id', 'study_id']
    merge_right = ['Study ID', 'Subj ID']
    if type == 'welders':
        merge_left.append('redcap_event_name')
        merge_right.append('Visit')

    merged_data = pd.merge(full_project,
                           ids,
                           left_on=merge_left,
                           right_on=merge_right)
    final_data = pd.merge(merged_data,
                          metabolites,
                          left_on=['PSU IEE ID'],
                          right_on=['PSU IEE'])
    return(final_data)


def _load_farmers():
    '''
    Load farmers databases concatenated

    Returns
    ----------
    full_project: pd.DataFrame
        Concatenated farmer databases
    '''
    project_files = glob.glob('../data/Project_*farmers.csv')
    exposures = get_exposures('farmers')
    covs = ['study_id',
            'research_subject',
            'age',
            'sex',
            'race',
            'ethnicity',
            'highest_education',
            'years_of_education']
    subject_replace = {1: 'Farmer',
                       3: 'Farmer',
                       2: 'Farmer Control',
                       4: 'Farmer Control'}
    project_data_list = []
    for file in project_files:
        project_data = pd.read_csv(file,
                                   sep=';')
        columns = covs + exposures
        if '42368' in file:
            replace_col_names = {'study_id_number': 'study_id'}
            project_data.rename(columns=replace_col_names,
                                inplace=True)
        project_data = replace_values(project_data,
                                      'research_subject',
                                      subject_replace)
        project_data = project_data.loc[:, columns]
        project_id = re.findall(r"\d+", file)
        project_data['project_id'] = int(project_id[0])
        project_data_list.append(project_data)

    full_project = pd.concat(project_data_list).reset_index(drop=True)
    # NA in exposures are 0
    full_project[exposures] = full_project[exposures].fillna(0)
    return(full_project)


def _load_welders(baseline=False,
                  non_retired_only=False):
    '''
    Load welders databases concatenated

    Parameters
    ----------
    baseline: bool
        Whether to return only baseline participants or not.
        Default False
    non_retired_only: bool
        Whether to return only non retired participants or not.
        Default False

    Returns
    ----------
    full_project: pd.DataFrame
        Concatenated welders databases
    '''
    project_files = glob.glob('../data/Project_*welders.csv')
    exposures = get_exposures('welders')
    covs = ['study_id',
            'redcap_event_name',
            'research_subject',
            'age',
            'sex',
            'race',
            'ethnicity',
            'highest_education',
            'years_of_education']
    visit_replace = {'baseline_arm_1': 1,
                     '18_month_followup_arm_1': 2,
                     '1_year_followup_arm_1': 2}
    project_data_list = []
    for file in project_files:
        project_data = pd.read_csv(file,
                                   sep=';')
        columns = covs + exposures
        if '5467' in file:
            # There are weird column names in this file
            replace_col_names = {'subject_id': 'study_id',
                                 'cohort': 'research_subject'}
            # Get the age
            age = get_age(project_data['blood_work_date'],
                          project_data['date_of_birth'])
            project_data['age'] = age
            # Keep certain rows
            keep = ~ (project_data['redcap_repeat_instance'] >= 1)
            project_data = project_data[keep]
            remove_from_list = ['race',
                                'years_of_education']
            columns = [i for i in columns if i not in remove_from_list]
            # Change type of research subject
            subject_replace = {1: 'Active',
                               2: 'Retired',
                               3: 'Control'}
            project_data.rename(columns=replace_col_names,
                                inplace=True)
        elif '37016' in file:
            # Change type of research subject
            subject_replace = {1: 'Active',
                               2: 'Control'}
        project_data = replace_values(project_data,
                                      'research_subject',
                                      subject_replace)
        project_data = project_data.loc[:, columns]
        project_id = re.findall(r"\d+", file)
        project_data['project_id'] = int(project_id[0])
        project_data_list.append(project_data)

    full_project = pd.concat(project_data_list).reset_index(drop=True)
    full_project = replace_values(full_project,
                                  'redcap_event_name',
                                  visit_replace)
    # NA in exposures are 0
    full_project[exposures] = full_project[exposures].fillna(0)
    if baseline:
        baseline = full_project['redcap_event_name'] == 1
        full_project = full_project.loc[baseline, :]

    if non_retired_only:
        non_retired = ~(full_project['research_subject'] == 'Retired')
        full_project = full_project.loc[non_retired, :]

    return(full_project)


def get_exposures(type: str = 'farmers'):
    '''
    Get a list of exposures depending on the type of data

    Parameters
    ----------
    type: str
        The type of data, either farmers or welders

    Returns
    ----------
    exposures: list of str
        A list of exposure columns
    '''
    if type == 'farmers':
        exposures = ['mixed_or_applied',
                     'years_mix_or_apply',
                     'days_mix_or_apply',
                     'percent_mix',
                     'percent_application',
                     'protective_equipment_new']
    elif type == 'welders':
        exposures = []
    else:
        raise ValueError('type should be farmers or welders')

    return(exposures)


def update_visit_info(data):
    '''
    Update the visit information from the project_IDs file.
    Some visit, even though are sequential (e.g. 4 and 5), dont'
    match the visit code used in other files (e.g. 1 and 2).

    Parameters
    ----------
    data: pd.DataFrame
        Dataframe with the uncorrected visit information

    Returns
    ----------
    corrected_data: pd.DataFrame
        Corrected dataframe
    '''
    for ind, dat in data.groupby(['Study ID', 'Subj ID']):
        if sum(dat['Visit']) > 3 and len(dat) > 1:
            data.iloc[dat.index[0], 5] = 1
            data.iloc[dat.index[1], 5] = 2

    return(data)


def replace_values(data: pd.DataFrame,
                   col_name: str,
                   to_replace: dict):
    '''
    Replace the values from a specific column in data based on to_replace dict

    Parameters
    ----------
    data: pd.DataFrame
        Data to replace the column with
    col_name: str
        Column name
    to_replace: dict
        Dictionary with the key and the value to replace the value with
    '''
    data[col_name] = data[col_name].replace(to_replace)
    return(data)


def get_age(collection_date,
            DOB):
    '''
    Get the age from the date of collection and DOB

    Parameters
    ----------
    collection_date: pd.DataFrame
        Column with collection date
    DOB: pd.DataFrame
        Date of Birth
    '''
    dob = pd.to_datetime(DOB,
                         format='%d/%m/%Y')
    doc = pd.to_datetime(collection_date,
                         format='%d/%m/%Y')
    days = doc - dob
    age = np.floor(days / np.timedelta64(1, 'Y'))
    return(age)
