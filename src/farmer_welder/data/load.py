# Load different data files for project
import re
import glob
import numpy as np
import pandas as pd


def load_data(type: str = 'farmers'):
    '''
    Load complete data for either farmers or welders

    Returns
    ----------
    dat: pd.DataFrame
        Data frame with complete data
    '''

    # READ DATA #
    ids = pd.read_csv('data/raw/project_IDs.csv')
    ids = update_visit_info(ids)
    metabolites = pd.read_csv('data/raw/metabolite_concentration.csv')

    if type == 'farmers':
        full_project = _load_farmers()
    elif type == 'welders':
        full_project = _load_welders()
        # Welder 36 is control
        id36 = full_project['study_id'] == 36
        full_project.loc[id36, 'research_subject'] = 'Control'
    else:
        raise ValueError('type should be farmers or welders')

    # MERGE DATA
    merge_left = ['project_id', 'study_id']
    merge_right = ['Study ID', 'Subj ID']
    if type == 'welders':
        merge_left.append('redcap_event_name')
        merge_right.append('redcap_event_name')

    first_merge = pd.merge(metabolites,
                           ids,
                           on=['PSU IEE'])

    final_data = pd.merge(full_project,
                          first_merge,
                          left_on=merge_left,
                          right_on=merge_right)
    return(final_data)


def _load_farmers():
    '''
    Load farmers databases concatenated

    Returns
    ----------
    full_project: pd.DataFrame
        Concatenated farmer databases
    '''
    project_files = glob.glob('data/raw/Project_*farmers.csv')
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


def _load_welders():
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
    project_files = glob.glob('data/raw/Project_*welders.csv')
    metal_names_5467 = get_metals()
    metal_names_37016 = get_metals(37016)
    replace_metals = dict(zip(metal_names_5467,
                              metal_names_37016))
    covs = ['study_id',
            'redcap_event_name',
            'research_subject',
            'age',
            'sex',
            'race',
            'ethnicity',
            'highest_education',
            'years_of_education',
            'currently_smoking',
            'elt']
    project_data_list = []
    columns = covs + metal_names_37016
    for file in project_files:
        project_data = pd.read_csv(file,
                                   sep=';')
        if '5467' in file:
            # Read metal levels 5467
            use_cols = metal_names_5467 + ['Subject ID']
            metal_5467 = pd.read_excel(
                'data/raw/Whole blood results all metals.xlsx',
                usecols=use_cols,
                skiprows=[i for i in range(78, 81)]).rename(replace_metals,
                                                            axis=1)
            non_baselines = metal_5467['Subject ID'].str.contains('flu')
            metal_5467['visit'] = 'baseline_arm_1'
            metal_5467.loc[non_baselines, 'visit'] = '18_month_followup_arm_1'
            metal_5467['Subject ID'] = metal_5467['Subject ID'].\
                str.replace('-flu18', '')
            metal_5467['Subject ID'] = metal_5467['Subject ID'].\
                astype('int64')

            # Merge metals
            project_data = pd.merge(project_data,
                                    metal_5467,
                                    how='left',
                                    left_on=['subject_id',
                                             'redcap_event_name'],
                                    right_on=['Subject ID',
                                              'visit'])
            # Convert Fe ug/ml to ug/L
            project_data.loc[:, 'fe'] = \
                project_data.loc[:, 'fe'] * 1000
            # There are weird column names in this file
            replace_col_names = {'subject_id': 'study_id',
                                 'cohort': 'research_subject'}
            # Get the age
            age = get_age(project_data['blood_work_date'],
                          project_data['date_of_birth'])
            project_data['age'] = age
            # Delete extra medication rows
            keep = ~ (project_data['redcap_repeat_instance'] >= 1)
            project_data = project_data[keep]
            remove_from_list = ['race',
                                'years_of_education']
            columns = [i for i in columns if i not in remove_from_list]
            # Change type of research subject
            subject_replace = {1: 'Active',
                               2: 'Retired',
                               3: 'Control'}
            project_data = project_data.rename(columns=replace_col_names)
            # Copy research subject info to non-baselines
            project_data = copy_from_baseline(project_data,
                                              'research_subject')
            # Read seq exposure data
            wh_exposure = pd.read_csv(
                'data/raw/UNC WH Exposure.csv').\
                rename(columns={'elt (mg-years/m3)':
                                'elt'})
            project_data = pd.merge(project_data,
                                    wh_exposure,
                                    how='left',
                                    left_on='study_id',
                                    right_on='subject_id')
            # Participants with NA in elt have zero
            project_data.loc[:, 'elt'] = project_data.loc[:, 'elt'].fillna(0)
        elif '37016' in file:
            # Change type of research subject
            subject_replace = {1: 'Active',
                               2: 'Control'}
            # Copy elt data from baseline to non-baseline
            project_data = copy_from_baseline(project_data,
                                              'elt')

        project_data = replace_values(project_data,
                                      'research_subject',
                                      subject_replace)
        project_data = project_data.loc[:, columns]
        project_id = re.findall(r"\d+", file)
        project_data['project_id'] = int(project_id[0])
        project_data_list.append(project_data)

    full_project = pd.concat(project_data_list).reset_index(drop=True)

    # NAs in smoking exposure are zero
    full_project['currently_smoking'] = full_project['currently_smoking'].\
        fillna(0)

    return(full_project)


def load_baseline_data(type: str = 'farmers'):
    '''
    Get the baseline data from welders or farmers

    Parameters
    ----------
    type: str
        The type of data, either farmers or welders

    Returns
    ----------
    baseline_data: pd.DataFrame
        Baseline dataframe
    '''
    if type == 'farmers':
        farmers = pd.read_csv('data/processed/farmers.csv')
        baseline_data = farmers.drop_duplicates(subset='Internal Code',
                                                keep='first')
    elif type == 'welders':
        welders = pd.read_csv('data/processed/welders.csv')
        non_duplicated = ~welders['Internal Code'].duplicated(keep=False)
        welders_nd = welders.loc[non_duplicated, :]
        welders_d = welders.loc[~non_duplicated, :]
        welders_d = welders_d.sort_values(by=['Internal Code', 'Visit'])
        welders_first = welders_d.drop_duplicates(subset='Internal Code',
                                                  keep='first')
        baseline_data = pd.concat([welders_nd, welders_first])
    else:
        raise ValueError('type should be farmers or welders')

    return(baseline_data)


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


def get_metabolites():
    '''
    Get list of metabolite names

    Returns
    ----------
    metabolties: list of str
        List of metabolite names
    '''
    metabolites = ['2-Oxoisocaproate', '3-Hydroxybutyrate',
                   '3-Hydroxyisovalerate', '3-Methyl-2-oxovalerate',
                   'Acetate', 'Acetone', 'Alanine', 'Citrate',
                   'Creatine', 'Formate', 'Glucose', 'Glutamine',
                   'Glycine', 'Histidine', 'Isoleucine', 'Lactate',
                   'Leucine', 'Lysine', 'Mannose', 'Phenylalanine',
                   'Pyruvate', 'Succinate', 'Threonine', 'Trimethylamine',
                   'Tryptophan', 'Tyrosine', 'Valine']
    return(metabolites)


def get_metals(study: int = 5467):
    '''
    Get the column names for the metal level measures
    that overlap across studies.

    Parameters
    ----------
    study: int
        Study, either 5467 or 37016
    '''
    if study == 5467:
        metals = ['whole blood Zn (ug/L)',
                  'whole blood Cu (ug/L)',
                  'whole blood Pb (ug/L)',
                  'whole blood Mn (ug/L)',
                  'whole blood Fe (ug/mL)']
    elif study == 37016:
        metals = ['zn',
                  'cu',
                  'pb',
                  'mn',
                  'fe']
    else:
        raise ValueError('Enter a valid study ID: 5467 or 37016')
    return(metals)


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


def copy_from_baseline(dat,
                       colname: str):
    '''
    Copy the baseline information in colname to the other rows

    Parameters
    ----------
    data: pd.DataFrame
        Data in which to copy
    colname: str
        Column name
    '''
    data = dat.copy()
    data = data.set_index('study_id')
    col = data.groupby('study_id')[colname].max()
    data = pd.merge(col,
                    data,
                    left_index=True,
                    right_index=True)
    col_to_drop = colname + '_y'
    col_to_change = colname + '_x'
    data = data.drop(col_to_drop,
                     axis=1)
    data = data.rename(columns={col_to_change:
                                colname})
    data = data.reset_index()
    return(data)
