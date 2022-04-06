import numpy as np


def euclidean_distance(mat: np.ndarray):
    '''
    Calculate the euclidean distances between
    all pairwise combinations from mat

    Parameters
    ----------
    mat: np.array
        Matrix to estimate all pairwise distances, with N rows, and P columns

    Returns
    ----------
    dist: np.array
        N x N distance matrix
    '''
    if not isinstance(mat, np.ndarray):
        mat = np.array(mat)
    n_rows = mat.shape[0]
    # Initialize an empty N x N distance matrix
    met_dist = np.zeros((n_rows, n_rows))
    # Calculate pairwise Euclidean distances
    for i in range(0, n_rows):
        n = i + 1
        for j in range(n, n_rows):
            p1 = mat[i, :]
            p2 = mat[j, :]
            dist = np.linalg.norm(p1 - p2)
            met_dist[i, j] = dist
            met_dist[j, i] = dist
    return met_dist
