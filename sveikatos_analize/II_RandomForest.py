import pandas as pd
from sklearn.metrics import recall_score, precision_score, f1_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt

import numpy as np

df = pd.read_csv('health-index-1.csv')

label_encoder = LabelEncoder()
df['country_ENCOD'] = label_encoder.fit_transform(df['country'])
X = df[['country_ENCOD', 'year']]
y = df['value']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

clf = RandomForestRegressor(random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)


importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]


plt.figure(figsize=(16, 6))
plt.title('Salies ir metu itaka sveikatos kokybei')
plt.xlabel('Svarbumas')
plt.ylabel('Parametras')
sns.barplot(x=importances[indices], y=X_train.columns[indices])
plt.show()

param_grid = {
    'n_estimators': [100, 200, 300],  #medziu sk
    'max_depth': [None, 10, 20],  # gylis
}
grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42),
                           param_grid=param_grid,
                           cv=5,
                           scoring='neg_mean_squared_error', #kuo reiksme mazesne, tuo modelis geresnis
                           n_jobs=-1)

grid_search.fit(X_train, y_train)

print('Best hyperparameters:', grid_search.best_params_)
print('Best result:', grid_search.best_score_)
