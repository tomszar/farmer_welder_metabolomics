# Create exploratory plots
from farmer_welder.data import load
from farmer_welder.stats import stats
from matplotlib.gridspec import GridSpec
from farmer_welder.visualization import figures

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def distribution_plots(dat: pd.DataFrame,
                       filename: str,
                       exposures: bool = True):
    """
    Generate violin plots with distribution of blood metal levels and metabolites.

    Parameters
    ----------
    dat: pd.DataFrame
        Dataset to use.
    filename: str
        Filename to use, including extension.
    exposures: bool
        Whether to plot the exposures. If False, plot metabolites
    """
    if exposures:
        variables = ['elt', 'e90', 'fe', 'mn', 'pb']
    else:
        variables = load.get_metabolites()
    grouping = dat.loc[:, 'Study ID'] == 37016
    fig = plt.figure(figsize=(10, len(variables) * 2),
                     dpi=300)
    gs = GridSpec(len(variables), 2, figure=fig)
    rows = np.repeat(list(range(0, len(variables))), 2)
    cols = [0, 1] * len(variables)
    count = 0
    for var in variables:
        ax1 = fig.add_subplot(gs[rows[count], cols[count]])
        count = count + 1
        ax2 = fig.add_subplot(gs[rows[count], cols[count]])
        transformed_dat = stats.transform_data(dat.loc[:, var],
                                               grouping=grouping,
                                               to_print=False)
        figures.concentration_violinplot(dat.loc[:, var],
                                         ax1,
                                         group_by=dat.loc[:, 'research_subject'])
        figures.concentration_violinplot(transformed_dat,
                                         ax2,
                                         group_by=dat.loc[:, 'research_subject'])
        count = count + 1
    fig.tight_layout()
    fig.savefig('results/figures/' + filename,
                dpi=300)


def correlation_plots(dat: pd.DataFrame,
                      filename: str):
    """
    Generate correlation plots with blood metal levels and metabolites.

    Parameters
    ----------
    dat: pd.DataFrame
        Dataset to use.
    filename: str
        Filename to use, including extension.
    """
    metabolites = load.get_metabolites()
    metals = ['elt', 'e90', 'fe', 'mn', 'pb']
    variables = metabolites + metals
    grouping = dat.loc[:, 'Study ID'] == 37016
    fig = plt.figure(figsize=(10, 10),
                     dpi=300)
    ax = fig.add_subplot(111)
    transformed_dat = stats.transform_data(dat.loc[:, variables],
                                           grouping=grouping,
                                           to_print=False)
    figures.correlation_plot(data=transformed_dat,
                             ax=ax,
                             labels=variables)
    fig.tight_layout()
    fig.savefig('results/figures/' + filename,
                dpi=300)


def main():
    """
    Main routine
    """
    print('=== Loading and transforming datasets ===')
    w_bs = load.load_baseline_data('welders')
    w_all = pd.read_csv('data/processed/welders.csv')
    print('\n=== Creating distribution plots ===')
    distribution_plots(w_bs, 'welders_baseline_exposures.png')
    distribution_plots(w_all, 'welders_total_exposures.png')
    distribution_plots(w_bs, 'welders_baseline_metabolites.png', False)
    distribution_plots(w_all, 'welders_total_metabolites.png', False)
    print('\n=== Creating correlation plots ===')
    correlation_plots(w_bs, 'welders_bs_corr.png')
    correlation_plots(w_all, 'welders_tot_corr.png')
