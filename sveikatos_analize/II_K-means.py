import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, silhouette_score
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


df = pd.read_csv('health-index-1.csv')

label_encoder = LabelEncoder()
df['country_encoded'] = label_encoder.fit_transform(df['country'])

X = df[['country_encoded', 'year']]
y = df['value']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print('mse', mse)
print('r2', r2)


plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', label='Predicted vs. Real')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Real Values')
plt.ylabel('Predicted Values')
plt.title('Predicted vs. Real Values')
plt.legend()



X = df[['country_encoded', 'value']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

clusters = [2, 3, 4, 5, 6, 7, 8, 9, 10]
s_scores = []

for n in clusters:
    kmeans = KMeans(n_clusters=n, random_state=0)
    kmeans.fit(X)
    silh_score = silhouette_score(X, kmeans.labels_)
    s_scores.append(silh_score)
    print(f'{n} clusters silhouette score: {silh_score:.2f}')
max_s_score_cluster = s_scores.index(max(s_scores)) + 3
print(f'\nThe best silhouette score is with {max_s_score_cluster} clusters')



kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)
clusters = kmeans.labels_



plt.figure(figsize=(8, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap='viridis')
plt.xlabel('Country (Standardized)')
plt.ylabel('Value (Standardized)')
plt.title('K-means Clustering')
plt.colorbar(label='Cluster')
plt.show()