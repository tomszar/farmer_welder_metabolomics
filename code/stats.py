# Module containing statistical functions
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def generate_PCA(D,
                 standardize=True):
    '''
    Generate a Principal Component Analysis

    Parameters
    ----------
    D: pd.DataFrame
        Data frame with metabolite concentration values
    standardize: bool
        Whether to standardize the values before or not.
        If False, it is assumed D contains standardize values

    Returns
    ----------
    pca_scores: pd.DataFrame
        Data frame with PCA scores
    '''
    if standardize:
        D_scaled = StandardScaler().fit(D).transform(D)
    else:
        D_scaled = D

    pca_scores = PCA(n_components=10).fit(D_scaled).transform(D_scaled)
    return(pca_scores)
