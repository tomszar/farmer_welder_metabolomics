import numpy as np
from scipy.stats import norm


def affinity_matrix(dist: np.ndarray,
                    k: int = 20,
                    sigma: float = 0.5):
    '''
    Generate an affinity matrix from a distance matrix

    Parameters
    ----------
    dist: np.array
        Distance matrix
    k: int
        Number of nearest neighbors (Recommended between 10 and 30)
    sigma: float
        Variance for local model
    '''
    if not isinstance(dist, np.ndarray):
        dist = np.array(dist)

    mach_eps = np.finfo(float).eps
    dist_mat = (dist + dist.transpose()) / 2
    np.fill_diagonal(dist_mat, 0)
    dist_mat_sort = np.sort(dist_mat, axis=0)
    means = np.mean(dist_mat_sort[1:k+1], axis=0) + mach_eps
    sig = (np.add.outer(means, means) / 2) / 3 * 2 + dist_mat / 3 + mach_eps
    sig[sig <= mach_eps] = mach_eps
    densities = norm.pdf(dist_mat, loc=0, scale=(sigma * sig))
    W = (densities + densities.transpose()) / 2
    return W
