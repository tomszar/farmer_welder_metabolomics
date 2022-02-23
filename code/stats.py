# Module containing statistical functions
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from sklearn.cross_decomposition import PLSRegression


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


def PLSR(X, y,
         p: int = 10,
         standardize_X: bool = True):
    '''
    Generate a Partial Leas Squares Regression

    Parameters
    ----------
    X: pd.DataFrame
        Metabolite concentration matrix
    Y: pd.DataFrame
        Exposure matrix
    p: int
        p participants left out for the leave-p-out cross-validation
    standardize_X: bool
        Whether to standardize the X matrix or not
    '''
    if standardize_X:
        X_scaled = StandardScaler().fit(X).transform(X)
    else:
        X_scaled = X

    encoder = OneHotEncoder(sparse=False)
    y_encoded = pd.DataFrame(encoder.fit_transform(y))
    y_encoded.columns = encoder.get_feature_names_out(y.columns)

    PLSDA = PLSRegression(n_components=5,
                          scale=False)
    scores = -1 * cross_val_score(PLSDA,
                                  X_scaled,
                                  y_encoded,
                                  cv=10,
                                  scoring='neg_mean_squared_error').mean()
    # x_scores, y_scores = PLSDA.fit_transform(X=X_scaled,
    #                                          y=y_encoded)
    return(scores)
