import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
import pickle

with open('..\data\processed_data.pickle', 'rb') as f:
    df = pickle.load(f)

# TODO: cross validation, grid search and stuff
y = df["attack_type"]
X = df.drop("attack_type", axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=24)
print("splitting finished")

rfc = RandomForestClassifier(n_jobs=-1, criterion='entropy')
rfc.fit(X_train, y_train)
y_pred = rfc.predict(X_test)
print("training finished")

# TODO: features could vary due to the inherent randomness, train many times get a intersection?union?appearance>50%?
importances = rfc.feature_importances_
indices = np.argsort(importances)
selected_feat_names = []
for f in range(X_train.shape[1]):
    if importances[indices[f]] != 0:
    # if importances[indices[f]] - 0.000001 > 0:
    # if f < 14:
        selected_feat_names.append(X.columns[f])
    print("%2d) %-*s %f" % (f + 1, 30, X.columns[f], importances[indices[f]]))

with open(r'..\data\feat_names.pickle', 'wb') as f:
    pickle.dump(selected_feat_names, f)

# TODO: more specific means measure a multi-class classification
print("precision: ", precision_score(y_true=y_test, y_pred=y_pred, average='macro'))

