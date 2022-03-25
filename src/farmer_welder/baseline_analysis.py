import argparse
import numpy as np
import pandas as pd
from .data import load
from .stats import stats
from .visualization import figures


def main():
    parser = argparse.ArgumentParser(description='Baseline analysis')
    parser.add_argument('cohort', help='Select either farmer or welder')
    args = parser.parse_args()

    if args.cohort == 'farmer':
        raise ValueError('No farmer analysis at this point')
    elif args.cohort == 'welder':
        welders = pd.read_csv('data/processed/welders.csv')
        non_duplicated = ~welders['Internal Code'].duplicated(keep=False)
        welders_nd = welders.loc[non_duplicated, :]
        welders_d = welders.loc[~non_duplicated, :]
        welders_d = welders_d.sort_values(by=['Internal Code', 'Visit'])
        welders_first = welders_d.drop_duplicates(subset='Internal Code',
                                                  keep='first')
        final_dat = pd.concat([welders_nd, welders_first])
        covs = ['age', 'sex', 'project_id', 'currently_smoking']
        outcomes = load.get_metabolites()
        metals = load.get_metals(37016)
    else:
        raise ValueError('Cohort should be farmer or welder')

    # Concentration violinplots
    metal_concentration = np.log2(final_dat[metals])
    concen = np.log2(final_dat.loc[:, outcomes] + 0.01)
    groups = final_dat['research_subject']
    figures.concentration_violinplot(concen,
                                     groups,
                                     filename='metabolites_welders_bs.pdf')
    figures.concentration_violinplot(metal_concentration,
                                     groups,
                                     filename='metals_welders_bs.pdf')
    replace_subjects = {'Retired': 'Welder',
                        'Active': 'Welder'}
    final_dat = final_dat.replace(replace_subjects)
    predictors = ['research_subject']
    res = stats.EWAS(outcomes,
                     covs,
                     predictors,
                     final_dat,
                     remove_outliers=True)
    res.to_csv('results/reports/welder_bs_binary.csv')
