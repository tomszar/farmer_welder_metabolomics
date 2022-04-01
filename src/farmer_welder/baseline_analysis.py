import argparse
from .data import load
from .stats import stats


def main():
    parser = argparse.ArgumentParser(description='Baseline analysis')
    parser.add_argument('cohort', help='Select either farmers or welders')
    args = parser.parse_args()
    # Read baseline data
    baseline_data = load.load_baseline_data(args.cohort)
    covs = ['age', 'sex', 'project_id', 'currently_smoking']
    outcomes = load.get_metabolites()
    # EWAS
    replace_subjects = {'Retired': 'Welder',
                        'Active': 'Welder'}
    final_dat = baseline_data.replace(replace_subjects)
    predictors = ['research_subject', 'elt', 'e90', 'hrsw', 'mn', 'pb', 'fe']
    names = ['_binary.csv',
             '_elt.csv',
             '_e90.csv',
             '_hrsw.csv',
             '_mn.csv',
             '_pb.csv',
             '_fe.csv']
    for study, dat in final_dat.groupby('Study ID'):
        if study == 37016:
            covs.append('years_of_education')
        for i, pred in enumerate(predictors):
            filename = 'results/reports/welder_bs_' +\
                str(study) + names[i]
            res = stats.EWAS(outcomes,
                             covs,
                             [pred],
                             dat,
                             remove_outliers=True)
            res.to_csv(filename)
