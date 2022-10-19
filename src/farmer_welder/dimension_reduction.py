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


# Get initial data
farmers_bs = load.load_baseline_data('farmers')
welders_bs = load.load_baseline_data('welders')
metabolites = load.get_metabolites()
exp_names_w = load.get_exposures('welders')
exp_names_f = load.get_exposures()
# Run PCA
pca = PCA()
X = stats.transform_data(welders_bs.loc[:, metabolites])
pca.fit(X)
print(pca.explained_variance_ratio_.round(3))

# Get contribution of variables
features = np.abs(pca.components_[1]).argsort()[::-1][:5]
print('List of metabolites that contribute to component 2')
print(np.array(metabolites)[features])

# Get all data
farmers_all = pd.read_csv('data/processed/farmers.csv')
welders_all = pd.read_csv('data/processed/welders.csv')
exp_welders = stats.transform_data(welders_all.loc[:, exp_names_w])
exp_famers = stats.transform_data(farmers_all.loc[:, exp_names_f])
welders_scores = get_PCA_scores(pca, welders_all.loc[:, metabolites])
farmers_scores = get_PCA_scores(pca, farmers_all.loc[:, metabolites])

for exp in exp_names_w:
    figures.plot_pca_scores(welders_scores,
                            continuous=exp_welders.loc[:, exp],
                            filename='PCA_welders_' + exp)

for g in ['research_subject', 'project_id']:
    figures.plot_pca_scores(welders_scores,
                            groups=welders_all.loc[:, g],
                            filename='PCA_welders_' + g)
    figures.plot_pca_scores(farmers_scores,
                            groups=farmers_all.loc[:, g],
                            filename='PCA_farmers_' + g)

for exp in exp_names_f:
    figures.plot_pca_scores(farmers_scores,
                            continuous=farmers_all.loc[:, exp],
                            filename='PCA_farmers_' + exp)
