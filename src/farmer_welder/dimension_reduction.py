# Creating a PCA space with baseline subset only
# Then projecting everyone onto that

from sklearn.decomposition import PCA
from farmer_welder.data import load
from farmer_welder.stats import stats
from farmer_welder.visualization import figures
import numpy as np
import pandas as pd


def get_PCA_scores(pca: PCA,
                   X: pd.DataFrame):
    '''
    Get PCA scores from a PCA on metabolites from a baseline.

    Parameters
    ----------
    pca: PCA
        PCA results from scikit.
    X: pd.DataFrame

    Returns
    -------
    scores: pd.DataFrame
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
    pca_w = PCA()
    pca_f = PCA()
    Xw = stats.transform_data(welders_bs.loc[:, metabolites])
    Xf = stats.transform_data(farmers_bs.loc[:, metabolites])
    pca_w.fit(Xw)
    pca_f.fit(Xf)
    print(pca_w.explained_variance_ratio_.round(3))
    print(pca_f.explained_variance_ratio_.round(3))

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
    print('Plots')
    print('Welders exposures')
    for exp in exp_names_w:
        figures.plot_pca_scores(welders_scores,
                                continuous=exp_welders.loc[:, exp],
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
