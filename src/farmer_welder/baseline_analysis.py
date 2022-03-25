import argparse
import numpy as np
from .data import load
from .stats import stats
from .visualization import figures


def main():
    parser = argparse.ArgumentParser(description='Baseline analysis')
    parser.add_argument('cohort', help='Select either farmers or welders')
    args = parser.parse_args()

    # Read baseline data
    baseline_data = load.load_baseline_data(args.cohort)
    covs = ['age', 'sex', 'project_id', 'currently_smoking']
    outcomes = load.get_metabolites()
    metals = load.get_metals(37016)
    # Concentration violinplots
    metal_concentration = np.log2(baseline_data[metals])
    concen = np.log2(baseline_data.loc[:, outcomes] + 0.01)
    groups = baseline_data['research_subject']
    figures.concentration_violinplot(concen,
                                     groups,
                                     filename='metabolites_welders_bs.pdf')
    figures.concentration_violinplot(metal_concentration,
                                     groups,
                                     filename='metals_welders_bs.pdf')
    # EWAS
    replace_subjects = {'Retired': 'Welder',
                        'Active': 'Welder'}
    final_dat = baseline_data.replace(replace_subjects)
    predictors = ['research_subject', 'elt']
    filename = ['welder_bs_binary.csv',
                'welder_bs_cont.csv']
    for i, pred in enumerate(predictors):
        res = stats.EWAS(outcomes,
                         covs,
                         [pred],
                         final_dat,
                         remove_outliers=True)
        res.to_csv('results/reports/' + filename[i])
