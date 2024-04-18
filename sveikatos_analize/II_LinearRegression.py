import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_selection import RFE
from math import sqrt

df = pd.read_csv('health-index-1.csv')

column_trans = ColumnTransformer(
    [('country_encoder', OneHotEncoder(), ['country'])],
    remainder='passthrough'
)

X = df[['country', 'year']]
y = df['value']

X_transformed = column_trans.fit_transform(X)

df_salis = df[df['country'] == 'Lithuania']
df_filtered_sorted = df_salis.sort_values('year')

X = df[['year', 'country']]
y = df[['value']]

X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
rmse = sqrt(mean_squared_error(y_test, y_pred))
print('MSE: ', mse)
print('R2: ', r2)
print('RMSE: ', rmse)

x_Lithuania = df_filtered_sorted[['year', 'country']]
X_country = column_trans.transform(df_filtered_sorted[['country', 'year']])
y_Lithuania_pred = model.predict(X_country)


n_features_optimal = 10
rfe = RFE(model, n_features_to_select=n_features_optimal)
rfe = rfe.fit(X_train, y_train)
y_pred = model.predict(X_test)



k_folds = KFold(n_splits= 5, shuffle=True, random_state=42)
scores = cross_val_score(model, X_transformed, y, cv=k_folds)

print("Cross Validation Scores: ", scores)
print("Average CV Score: ", scores.mean())
print("Number of CV Scores used in Average: ", len(scores))

plt.scatter(df_filtered_sorted['year'], df_filtered_sorted['value'], color='blue', label='Mokymo duomenys', s=10)
plt.plot(df_filtered_sorted['year'], y_Lithuania_pred, linestyle='--', marker='o', color='red', label='Prognoze')
plt.xlabel('Metai')
plt.ylabel('Value')
plt.title('Sveikatos indekso prognoze pagal metus - Lietuva')
plt.legend()
plt.grid(True)
plt.show()
