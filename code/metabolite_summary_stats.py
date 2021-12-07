import figures
import numpy as np
import pandas as pd

metab = pd.read_csv('../data/metabolite_concentration.csv')
concen = np.log2(metab.iloc[:, 4:])

# Violin plot
figures.concentration_violinplot(concen)
