import numpy as np
import pandas as pd
from kmodes.kmodes import KModes
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv('health-index-1.csv')

V_Y = df[['value', 'year']]


scaler = StandardScaler()
X_scaled = scaler.fit_transform(V_Y)
dbscan = DBSCAN(eps=0.2, min_samples=8)
clusters = dbscan.fit_predict(X_scaled)
df['cluster'] = clusters



plt.figure(figsize=(10, 6))
plt.scatter(df['value'], df['year'], c=df['cluster'], cmap='viridis')
plt.scatter(df['value'][clusters == -1], df['year'][clusters == -1], c='red', marker='x', label='Noise')
plt.title("Sveikatos duomenu rinkimo daznumas pagal /value/ ir /year/ - DBSCAN")
plt.xlabel("Pagal values")
plt.ylabel("Year")
plt.colorbar(label='cluster')
plt.show()