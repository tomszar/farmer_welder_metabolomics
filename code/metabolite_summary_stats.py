import load
import stats
import figures
import numpy as np
import pandas as pd

metab = pd.read_csv('../data/metabolite_concentration.csv')
concen = np.log2(metab.iloc[:, 4:] + 0.01)

# Violin plot
figures.concentration_violinplot(concen)

# PCA
pca_scores = stats.generate_PCA(concen)
figures.plot_pca_scores(pca_scores)

# Complete dataset
dat = load.load_complete_data()
dat.to_csv('../results/merged_data.csv',
           index=False)
