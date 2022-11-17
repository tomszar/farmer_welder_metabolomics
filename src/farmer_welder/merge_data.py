from farmer_welder.data import load
from farmer_welder.data import clean


def main():
    farmers = load.load_raw_data('farmers')
    welders = load.load_raw_data('welders')
    welders = clean.transform_education(welders)

    # print basic information
    print('=== Basic information in welders ===')
    for project, dat in welders.groupby('project_id'):
        print(f'In project {project}:')
        dat = dat.set_index('study_id')
        unique_dat = dat.loc[~dat.index.duplicated(), :]
        repeated_dat = dat.loc[dat.index.duplicated(), :]
        unique_ids = dat.index.unique()
        non_unique = dat.shape[0] - len(unique_ids)
        print(f'There are {len(unique_ids)} unique participants and \
{non_unique} non unique')
        print('From the whole dataset, the samples are splitted like this:')
        print(dat.loc[:, 'research_subject'].value_counts())
        print('From the unique dataset, the samples are splitted like this:')
        print(unique_dat.loc[:, 'research_subject'].value_counts())
        print('From the repeated dataset, the samples are splitted like this:')
        print(repeated_dat.loc[:, 'research_subject'].value_counts(), '\n')
        cols_na = ['age', 'sex', 'race', 'ethnicity', 'years_of_education',
                   'smoked_regularly', 'zn', 'cu', 'pb', 'mn', 'fe', 'elt',
                   'e90', 'hrsw']
        cols_mean = ['age', 'years_of_education', 'zn', 'cu', 'pb', 'mn', 'fe',
                     'elt', 'e90', 'hrsw']
        for col in cols_na:
            nas = welders.loc[:, col].isna().sum()
            print(f'In column {col} there are {nas} missing values.')
        print('')
        for subject, dat2 in dat.groupby('research_subject'):
            print(f'Mean values for {subject}')
            for col in cols_mean:
                mean = dat2.loc[:, col].mean().round(2)
                print(f'Mean value for {col}: {mean}')
            print('')

    farmers.to_csv('data/processed/farmers.csv',
                   index=False)
    welders.to_csv('data/processed/welders.csv',
                   index=False)
    print('Farmer and Welder data consolidated\n')
