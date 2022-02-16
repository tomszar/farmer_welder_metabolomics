# Load different data files for project
import re
import glob
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
    ids = pd.read_csv('../data/project_IDs.csv')
    metabolites = pd.read_csv('../data/metabolite_concentration.csv')
    if type == 'farmers':
        project_files = glob.glob('../data/Project_*farmers.csv')
        covs = ['study_id',
                'research_subject',
                'age',
                'sex',
                'race',
                'ethnicity',
                'highest_education',
                'years_of_education']
        exposures = ['mixed_or_applied',
                     'years_mix_or_apply',
                     'days_mix_or_apply',
                     'percent_mix',
                     'percent_application',
                     'protective_equipment_new']
        subject_replace = {1: 'Farmer',
                           3: 'Farmer',
                           2: 'Farmer Control',
                           4: 'Farmer Control'}
    elif type == 'welders':
        project_files = glob.glob('../data/Project_*welders.csv')
    else:
        raise ValueError('type should be farmers or welders')

    project_data_list = []

    for file in project_files:
        columns = covs + exposures
        if '42368' in file:
            columns[0] = 'study_id_number'
        elif '37016' in file:
            columns.append('redcap_event_name')
        elif '5467' in file:
            # There are weird column names in this file
            columns[0] = 'subject_id'
            columns[1] = 'cohort'
        project_data = pd.read_csv(file,
                                   sep=';').loc[:, columns]
        project_data.rename(columns={'study_id_number': 'study_id'},
                            inplace=True)
        # if '37016' in file:
        #    project_data.rename(columns={'redcap_event_name': 'visit'},
        #                        inplace=True)
        #    project_data.visit.replace('baseline_arm_1', 1,
        #                               inplace=True)
        #    project_data.visit.replace('1_year_followup_arm_1', 2,
        #                               inplace=True)
        # else:
        #    project_data['visit'] = 1
        project_id = re.findall(r"\d+", file)
        project_data['project_id'] = project_id[0]
        project_data_list.append(project_data)

    full_project = pd.concat(project_data_list).reset_index(drop=True)
    full_project['project_id'] = full_project['project_id'].astype('int64')
    full_project['research_subject'] = full_project['research_subject'].\
        replace(subject_replace)
    # NA in exposures are 0
    full_project[exposures] = full_project[exposures].fillna(0)

    # MERGE DATA
    merged_data = pd.merge(full_project,
                           ids,
                           left_on=['project_id', 'study_id'],
                           right_on=['Study ID', 'Subj ID'])
    final_data = pd.merge(merged_data,
                          metabolites,
                          left_on=['PSU IEE ID'],
                          right_on=['PSU IEE'])
    return(final_data)
