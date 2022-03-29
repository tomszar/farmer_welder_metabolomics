import argparse
import numpy as np
import pandas as pd
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
    exposure_concentration = baseline_data.loc[:, ['elt',
                                                   'e90']]
    hrsw_concentration = baseline_data.loc[:, 'hrsw']
    concen = np.log2(baseline_data.loc[:, outcomes] + 0.01)
    names = ['metabolites', 'metals', 'exposures', 'hrsw']
    xlabels = ['Log2 concentration', 'Log2 concentration',
               'Exposure value', 'Hours welding']
    titles = ['Metabolite concentrations',
              'Metal concentrations',
              'Exposure metrics',
              'Hours welding']
    for i, data in enumerate([concen,
                              metal_concentration,
                              exposure_concentration,
                              hrsw_concentration]):
        data_with_id = pd.concat([data, baseline_data[['Study ID',
                                                       'research_subject']]],
                                 axis=1)
        for study, dat in data_with_id.groupby('Study ID'):
            title = titles[i] + ' ' + str(study)
            groups = dat['research_subject']
            dat_dropped = dat.drop(['Study ID', 'research_subject'], axis=1)
            filename = names[i] + '_welders_bs_' + str(study) + '.pdf'
            figures.concentration_violinplot(dat_dropped,
                                             groups,
                                             filename=filename,
                                             xlabel=xlabels[i],
                                             title=title)
    # EWAS
    replace_subjects = {'Retired': 'Welder',
                        'Active': 'Welder'}
    final_dat = baseline_data.replace(replace_subjects)
    predictors = ['research_subject', 'elt', 'e90', 'hrsw', 'pb']
    names = ['_binary.csv',
             '_elt.csv',
             '_e90.csv',
             '_hrsw.csv',
             '_pb.csv']
    for study, dat in final_dat.groupby('Study ID'):
        for i, pred in enumerate(predictors):
            filename = 'results/reports/welder_bs_' +\
                str(study) + names[i]
            res = stats.EWAS(outcomes,
                             covs,
                             [pred],
                             dat,
                             remove_outliers=True)
            res.to_csv(filename)
