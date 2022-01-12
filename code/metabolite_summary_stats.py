import load
import stats
import figures
import numpy as np
from scipy.stats import linregress

dat = load.load_complete_data()
concen = np.log2(dat.iloc[:, 21:] + 0.01)
groups = np.array(dat['research_subject'])

# Violin plot
figures.concentration_violinplot(concen)

# PCA
pca_scores = stats.generate_PCA(concen)
figures.plot_pca_scores(pca_scores,
                        groups=groups)
figures.plot_pca_scores(pca_scores,
                        continuous=dat['age'],
                        filename='metabolites_pca_age')

# Regression
welders = dat.query('research_subject==1 or research_subject==2')
x = welders['research_subject']
y = np.log2(welders['Glycine'] + 0.01)
b = ~np.isnan(x)
slope, intercept, r, p, se = linregress(x[b], y[b])

# Complete dataset
dat.to_csv('../results/merged_data.csv',
           index=False)
