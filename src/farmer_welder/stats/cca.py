from sklearn.model_selection import LeaveOneOut
from sklearn.pipeline import make_pipeline
from sklearn.cross_decomposition import CCA
from sklearn import preprocessing
import numpy as np


def cca(X: np.ndarray,
        Y: np.ndarray):
    '''
    Run a Canonical Correlation Analysis (CCA). Make sure that
    X and Y matrices are only log-transformed if necessary, but
    not standardized.

    Parameters
    ----------
    X: np.ndarray
        X matrix
    Y: np.ndarray
        Y matrix
    '''
    clf = make_pipeline(preprocessing.StandardScaler(), CCA(C=1))
