import load
import stats
import figures
import numpy as np

farmers = load.load_data('farmers')
concen = np.log2(farmers.iloc[:, 26:] + 0.01)
groups = farmers['research_subject']

farmers.to_csv('../results/farmers.csv',
               index=False)
# Violin plot
figures.concentration_violinplot(concen,
                                 groups,
                                 filename='metabolites_grouped.pdf')

figures.concentration_violinplot(concen,
                                 filename='metabolites_total.pdf')

# PCA
pca_scores = stats.generate_PCA(concen)
figures.plot_pca_scores(pca_scores,
                        groups=groups)
figures.plot_pca_scores(pca_scores,
                        continuous=farmers['age'],
                        filename='metabolites_pca_age')
