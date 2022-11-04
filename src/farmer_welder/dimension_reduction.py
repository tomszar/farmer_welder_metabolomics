# Creating a PCA space with baseline subset only
# Then projecting everyone onto that
import numpy as np
import pandas as pd

from typing import Union
from sklearn.decomposition import PCA
from farmer_welder.data import load
from farmer_welder.stats import stats
from farmer_welder.visualization import figures


def run_PCA(dat: pd.DataFrame,
            transform: bool = True,
            grouping: Union[list[bool], None] = None) -> PCA:
    '''
    Run PCA on dataset

    Parameters
    ----------
    dat: pd.DataFrame
        Dataframe to apply the PCA.
    transform: bool
        Whether to apply transformation to the dataset or not (log2 and zscore)
    grouping: Union[list[bool], None]
        List of boolean with groupings to separate dataset.

    Returns
    -------
    pca: PCA
       PCA results
    '''
    pca = PCA()
    if transform:
        dat = stats.transform_data(dat,
                                   grouping=grouping)
    pca.fit(dat)
    print(pca.explained_variance_ratio_.round(3))
    return pca


def get_PCA_scores(pca: PCA,
                   X: pd.DataFrame) -> np.ndarray:
    '''
    Get PCA scores from a PCA on metabolites from a baseline.

    Parameters
    ----------
    pca: PCA
        PCA results from scikit.
    X: pd.DataFrame

    Returns
    -------
    scores: np.ndarray
        PCA scores obtained from projecting onto the PCA space.
    '''
    X = stats.transform_data(X)
    scores = pca.transform(X)
    return scores


def print_contributing_vars(pca: PCA,
                            component: int,
                            variables: list[str],
                            suffix: str):
    '''
    Print the top 5 variables that contribute to the specified component.

    Parameters
    ----------
    pca: PCA
        PCA results from scikit.
    component: int
        Number of component to evaluate.
    variables: list[str]
        List of variables used in the PCA.
    suffix: str
        String to append at the end of printing statement.
    '''
    features = np.abs(pca.components_[component - 1]).argsort()[::-1][:5]
    print(f'List of metabolites that contribute to component {component} ' +
          f'in {suffix}')
    print(np.array(variables)[features])


def get_groupings(dat: pd.DataFrame,
                  col: str) -> list[bool]:
    '''
    Get groupings from a specified column.

    Parameters
    ----------
    dat: pd.DataFrame
        Dataframe to obtain the groupings.
    col: str
        Column to use for groupings.

    Returns
    -------
    groupings: list[bool]
        List of bool with groupings.
    '''
    groups = dat.loc[:, col].unique()
    grouping = dat.loc[:, col] == groups[0]
    return grouping


def main():
    '''
    Main routine.
    '''
    # Get initial data
    print('Getting baseline data and running PCA')
    farmers_bs = load.load_baseline_data('farmers')
    welders_bs = load.load_baseline_data('welders')
    metabolites = load.get_metabolites()
    exp_names_w = load.get_exposures('welders')
    exp_names_f = load.get_exposures()
    # Run PCA
    grouping_w = get_groupings(welders_bs,
                               'project_id')
    grouping_f = get_groupings(farmers_bs,
                               'project_id')
    pca_w = run_PCA(welders_bs.loc[:, metabolites],
                    grouping=grouping_w)
    pca_f = run_PCA(farmers_bs.loc[:, metabolites],
                    grouping=grouping_f)
    # Get contribution of variables
    print_contributing_vars(pca_w, 2, metabolites, 'welders')
    print_contributing_vars(pca_f, 2, metabolites, 'farmers')

    # Get all data
    print('Getting all data and projecting PCA')
    farmers_all = pd.read_csv('data/processed/farmers.csv')
    welders_all = pd.read_csv('data/processed/welders.csv')
    print('Transforming exposures')
    exp_welders = stats.transform_data(welders_all.loc[:, exp_names_w])
    print('Transforming metabolites')
    welders_scores = get_PCA_scores(pca_w, welders_all.loc[:, metabolites])
    farmers_scores = get_PCA_scores(pca_f, farmers_all.loc[:, metabolites])
    print(welders_scores)
    print('Plots')
    print('Welders exposures')
    for exp in exp_names_w:
        figures.plot_pca_scores(welders_scores,
                                #continuous=exp_welders.loc[:, exp], # -> This is not working!!
                                filename='PCA_welders_' + exp)
    print('Research subjects')
    for g in ['research_subject', 'project_id']:
        figures.plot_pca_scores(welders_scores,
                                groups=welders_all.loc[:, g],
                                filename='PCA_welders_' + g)
        figures.plot_pca_scores(farmers_scores,
                                groups=farmers_all.loc[:, g],
                                filename='PCA_farmers_' + g)
    print('Farmer exposures')
    for exp in exp_names_f:
        print(exp)
        figures.plot_pca_scores(farmers_scores,
                                continuous=farmers_all.loc[:, exp],
                                filename='PCA_farmers_' + exp)
    print('Farmer covariates')
    for var in ['total_score',
                'alcoholic_drinks',
                'cigarettes',
                'smoked_regularly',
                'still_smoke',
                'age']:
        print(var)
        if var in ['total_score', 'age']:
            # Remove NA from this variable
            if var == 'total_score':
                keep_non_nas = ~farmers_all.loc[:, 'total_score'].isna()
            else:
                keep_non_nas = ~farmers_all.loc[:, 'age'].isna()
            figures.plot_pca_scores(farmers_scores[keep_non_nas, :],
                                    continuous=farmers_all.loc[keep_non_nas,
                                                               var],
                                    filename='PCA_farmers_' + var)
        else:
            figures.plot_pca_scores(farmers_scores,
                                    groups=farmers_all.loc[:, var],
                                    filename='PCA_farmers_' + var)
    print('Welder covariates')
    for var in ['currently_smoking',
                'cognitive_impairment',
                'age',
                'upsit_score',
                'mmse_total_score']:
        if var in ['age', 'upsit_score', 'mmse_total_score']:
            figures.plot_pca_scores(welders_scores,
                                    continuous=welders_all.loc[:, var],
                                    filename='PCA_welders_' + var)
        else:
            figures.plot_pca_scores(welders_scores,
                                    groups=welders_all.loc[:, var],
                                    filename='PCA_welders_' + var)
