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


farmers_bs = load.load_baseline_data('farmers')
welders_bs = load.load_baseline_data('welders')
metabolites = load.get_metabolites()
exp_welders = load.get_exposures('welders')
pca = PCA()
X = stats.transform_data(welders_bs.loc[:, metabolites])
pca.fit(X)
print(pca.explained_variance_ratio_.round(3))

# Get contribution of variables
features = np.abs(pca.components_[1]).argsort()[::-1][:5]
print('List of metabolites that contribute to component 2')
print(np.array(metabolites)[features])

farmers_all = pd.read_csv('data/processed/farmers.csv')
welders_all = pd.read_csv('data/processed/welders.csv')

exposures = stats.transform_data(welders_all.loc[:, exp_welders])
welders_scores = get_PCA_scores(pca, welders_all.loc[:, metabolites])
farmers_scores = get_PCA_scores(pca, farmers_all.loc[:, metabolites])

figures.plot_pca_scores(welders_scores,
                        continuous=exposures.loc[:, 'e90'],
                        filename='PCA_welders_e90')

figures.plot_pca_scores(welders_scores,
                        continuous=exposures.loc[:, 'elt'],
                        filename='PCA_welders_elt')

figures.plot_pca_scores(welders_scores,
                        groups=welders_all.loc[:, 'research_subject'],
                        filename='PCA_welders_groups')

figures.plot_pca_scores(welders_scores,
                        groups=welders_all.loc[:, 'project_id'],
                        filename='PCA_welders_project')

figures.plot_pca_scores(welders_scores,
                        continuous=welders_all.loc[:, 'age'],
                        filename='PCA_welders_age')

full_welders = pd.concat([welders_all, pd.DataFrame(welders_scores)], axis=1)
full_welders.to_csv('results/Welder_scores.csv')
