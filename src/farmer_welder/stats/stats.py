import clarite
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch

from typing import Union
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
        dat_clean.loc[:, outcomes] + (1 / 100000000))
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
                                            min_n=10,
                                            standardize_data=True)

    return(res)


def transform_data(data: Union[pd.DataFrame, pd.Series],
                   log2_transform: bool = True,
                   zscore_transform: bool = True):
    '''
    Zscore normalize dataframe

    Parameters
    ----------
    data: pd.DataFrame or pd.Series
        Data to normalize

    Returns
    ----------
    transformed_data: pd.DataFrame
        Transformed data
    '''
    print('=== Transforming data ===')
    transformed_data = data.copy()
    if log2_transform:
        print('Log2 transformation ...')
        transformed_data = np.log2(transformed_data + (1 / 100000000))

    if zscore_transform:
        print('Zscore transformation ...')
        if isinstance(transformed_data, pd.DataFrame):
            for col in transformed_data.columns:
                transformed_data[col] = (transformed_data[col] -
                                         transformed_data[col].mean()) \
                    / transformed_data[col].std()
        elif isinstance(transformed_data, pd.Series):
            transformed_data = (transformed_data -
                                transformed_data.mean()) \
                / transformed_data.std()

    print('')
    return transformed_data


def cluster_corr(corr_array):
    '''
    Rearranges the correlation matrix, corr_array, so that groups of highly
    correlated variables are next to each other.

    Parameters
    ----------
    corr_array: pd.DataFrame or np.ndarray
        a NxN correlation matrix

    Returns
    ----------
    idx: index
        a N index to rearrange columns and rows
    '''
    pairwise_distances = sch.distance.pdist(corr_array)
    linkage = sch.linkage(pairwise_distances,
                          method='complete')
    cluster_distance_threshold = pairwise_distances.max()/2
    idx_to_cluster_array = sch.fcluster(linkage,
                                        cluster_distance_threshold,
                                        criterion='distance')
    idx = np.argsort(idx_to_cluster_array)
    return idx
