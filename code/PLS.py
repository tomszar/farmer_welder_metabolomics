import load
import stats
import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder, scale
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import LeavePOut

farmers = load.load_data('farmers')
exposures = farmers.iloc[:, 8:14]
exposure = exposures.iloc[:,0]
concen = np.log2(farmers.iloc[:, 26:] + 0.01)
concen = scale(concen)

lpo = LeavePOut(10)
lpo.get_n_splits(concen)

i = 0
for train_index, test_index in lpo.split(concen):
    X_train, X_test = concen[train_index], concen[test_index]
    y_train, y_test = exposure[train_index], exposure[test_index]
    PLSDA = PLSRegression(n_components=1,
                          scale=False)
    PLSDA.fit(X_train, y_train)
    y_pred = PLSDA.predict(X_test)
    i = i + 1

scores = stats.PLSR(concen, exposures, standardize_X=False)

encoder = OneHotEncoder(sparse=False)
Y = pd.DataFrame(encoder.fit_transform(exposures))
Y.columns = encoder.get_feature_names_out(exposures.columns)

PLSDA = PLSRegression(n_components=5,
                      scale=False).\
    fit_transform(X=concen,
                  y=Y)
