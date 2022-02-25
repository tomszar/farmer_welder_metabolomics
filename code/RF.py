import load
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report

farmers = load.load_data('farmers')
exposures = farmers.iloc[:, 8:14]
concen = farmers.iloc[:, 26:]
X = np.array(concen)
y = farmers['research_subject']
subject_replace = {'Farmer': 1,
                   'Farmer Control': 0}
y = y.replace(subject_replace)

# Grid Search
scoring = ('f1', 'recall', 'precision')
SRF = RandomForestClassifier(class_weight='balanced_subsample',
                             random_state=6739)
param_grid = {
    'n_estimators': [100, 150, 200],
    'max_features': ['auto', 'sqrt', 'log2'],
    'min_samples_split': [2, 3, 4],
    'min_samples_leaf': [1, 2, 3],
    'criterion': ['gini', 'entropy']
}
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1652)
CV_rfc = GridSearchCV(estimator=SRF,
                      param_grid=param_grid,
                      scoring=scoring,
                      refit='f1',
                      cv=5)
CV_rfc.fit(X, y)
CV_rfc.best_params_

# Evaluate best parameters
SRF = RandomForestClassifier(n_estimators=200,
                             class_weight='balanced_subsample',
                             random_state=6739)
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.1,
                                                    random_state=1384,
                                                    stratify=y)
SRF.fit(X_train, y_train)
y_pred = SRF.predict(X_test)
print(classification_report(y_test, y_pred))
