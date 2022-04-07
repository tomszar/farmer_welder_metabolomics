from sklearn.metrics.pairwise import euclidean_distances,\
                                     nan_euclidean_distances
from farmer_welder.data import load
from farmer_welder.stats import affinity, stats
from farmer_welder.visualization import figures
import numpy as np

mach_eps = np.finfo(float).eps
bs = load.load_baseline_data('welders')
metabolites = load.get_metabolites()
exposures = load.get_exposures('welders')
metals = load.get_metals(37016)
old_study = bs[bs['project_id'] == 37016]

dist_metabolites = euclidean_distances(stats.
                                       transform_data(old_study[metabolites] +
                                                      mach_eps))
dist_exposures = euclidean_distances(stats.transform_data(old_study[exposures],
                                                          log2_transform=False))
dist_metals = nan_euclidean_distances(stats.transform_data(old_study[metals]))

W1 = affinity.affinity_matrix(np.power(dist_metabolites, 2))
W2 = affinity.affinity_matrix(np.power(dist_exposures, 2))
W3 = affinity.affinity_matrix(np.power(dist_metals, 2))

figures.correlation_plot(W1, estimate_corr=False,
                         filename='affinity_matrix_metabolites.png')
figures.correlation_plot(W2, estimate_corr=False,
                         filename='affinity_matrix_exposures.png')
figures.correlation_plot(W3, estimate_corr=False,
                         filename='affinity_matrix_metals.png')
