import load
import numpy as np
from sklearn.preprocessing import scale
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LeavePOut
from sklearn import metrics

farmers = load.load_data('farmers')
exposures = farmers.iloc[:, 8:14]
concen = np.log2(farmers.iloc[:, 26:] + 0.01)
X = scale(concen)
y = exposures.iloc[:, 0]
lpo = LeavePOut(2)

accuracy = []
for train_index, test_index in lpo.split(concen):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    clf = RandomForestClassifier(n_estimators=100,
                                 min_samples_split=2,
                                 random_state=10293,
                                 verbose=0)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = metrics.accuracy_score(y_test, y_pred)
    accuracy.append(acc)
