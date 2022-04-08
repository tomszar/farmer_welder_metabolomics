from farmer_welder.stats import cca
from farmer_welder.data import load
import numpy as np

from sklearn.model_selection import LeavePOut, KFold
from sklearn.cross_decomposition import CCA
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing


mach_eps = np.finfo(float).eps
bs = load.load_baseline_data('welders')
metabolites = load.get_metabolites()
exposures = load.get_exposures('welders')
metals = load.get_metals(37016)
old_study = bs[bs['project_id'] == 37016]

X = np.array(old_study[metabolites])
X2 = np.array(old_study[metals])
Y = np.array(old_study[exposures])

X = np.log2(X + mach_eps)
Y = np.log2(Y + mach_eps)

kf = KFold(n_splits=10)
lpo = LeavePOut(5)
cca = CCA(n_components=3, scale=True)
# scores = cross_val_score(cca, X, Y, cv=lpo)
scores = []
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    X_train = preprocessing.StandardScaler().fit(X_train).transform(X_train)
    X_test = preprocessing.StandardScaler().fit(X_test).transform(X_test)
    Y_train, Y_test = Y[train_index], Y[test_index]
    Y_train = preprocessing.StandardScaler().fit(Y_train).transform(Y_train)
    Y_test = preprocessing.StandardScaler().fit(Y_test).transform(Y_test)
    cca.fit(X_train, Y_train)
    X_c, Y_c = cca.transform(X_test, Y_test)
    coef = np.corrcoef(X_c[:, 0], Y_c[:, 0])
    scores.append(coef[0][1])
