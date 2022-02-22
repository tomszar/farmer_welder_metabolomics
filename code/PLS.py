import load
import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder, scale
from sklearn.cross_decomposition import PLSRegression

farmers = load.load_data('farmers')
exposures = farmers.iloc[:, 9:14]
concen = np.log2(farmers.iloc[:, 26:] + 0.01)
concen = scale(concen)

encoder = OneHotEncoder(sparse=False)
Y = pd.DataFrame(encoder.fit_transform(exposures))
Y.columns = encoder.get_feature_names_out(exposures.columns)

PLSDA = PLSRegression(n_components=5,
                      scale=False).\
    fit_transform(X=concen,
                  y=Y)
