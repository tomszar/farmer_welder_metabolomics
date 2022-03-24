import clarite
import numpy as np
import pandas as pd
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
    pca: PCA
        PCA object
    '''
    if standardize:
        D_scaled = StandardScaler().fit(D).transform(D)
    else:
        D_scaled = D

    pca = PCA(n_components='mle').fit(D_scaled)
    return(pca)


def EWAS(outcomes: list[str],
         covariates: list[str],
         predictors: list[str],
         data: pd.DataFrame,
         remove_outliers: bool = False):
    '''
    Run an environment-wide association study

    Parameters
    ----------
    outcomes: list of str
        List of column names for the outcomes to use
    covariates: list of str
        List of column names for the covariates to use
    predictors: list of str
        List of column names for the predictors to use
    data: pd.DataFrame
        Data frame to use
    remove_outliers: bool
        Whether to remove outliers before the EWAS. Default False
    '''
    dat_clean = data.loc[:, covariates + predictors + outcomes]
    # Log2 and normalize
    dat_clean.loc[:, outcomes] = np.log2(
        dat_clean.loc[:, outcomes] + 0.01)
    dat_clean = clarite.modify.categorize(dat_clean)
    var_types = clarite.describe.get_types(dat_clean)
    var_unknown = var_types[var_types == 'unknown'].index
    dat_clean = clarite.modify.make_continuous(dat_clean,
                                               only=var_unknown)
    if remove_outliers:
        dat_clean.loc[:, outcomes] = clarite.modify.remove_outliers(
            dat_clean.loc[:, outcomes])
    res = clarite.analyze.association_study(outcomes=outcomes,
                                            covariates=covariates,
                                            regression_variables=predictors,
                                            data=dat_clean,
                                            min_n=50,
                                            standardize_data=True)

    return(res)