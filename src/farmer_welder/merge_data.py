from .data import load


def main():
    farmers = load.load_raw_data('farmers')
    welders = load.load_raw_data('welders')

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

    farmers.to_csv('data/processed/farmers.csv',
                   index=False)
    welders.to_csv('data/processed/welders.csv',
                   index=False)
    print('Farmer and Welder data consolidated\n')
