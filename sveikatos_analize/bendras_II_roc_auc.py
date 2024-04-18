from sklearn.compose import ColumnTransformer
from sklearn.metrics import roc_curve, auc
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


df = pd.read_csv('health-index-1.csv')

label_encoder = LabelEncoder()
df['country_encoded'] = label_encoder.fit_transform(df['country'])
df['value'] = (df['value'] > 0.5).astype(int)
column_trans = ColumnTransformer([('country_encoded', OneHotEncoder(),['country_encoded'])], remainder='passthrough')

X = df[['year', 'country_encoded']]
y = df[['value']]
X_transform = column_trans.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_transform, y, test_size=0.3, random_state=42)
clf = LogisticRegression(random_state=42, max_iter=1000)
clf.fit(X_train, y_train)



y_scores = clf.predict_proba(X_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, y_scores)
roc_auc = auc(fpr, tpr)
print(f"AUC: {roc_auc}")

plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area =%0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve')
plt.legend(loc="lower right")
plt.show()