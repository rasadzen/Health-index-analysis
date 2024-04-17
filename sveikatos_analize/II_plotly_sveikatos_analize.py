import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer

df = pd.read_csv('health-index-1.csv')


label_encoder = LabelEncoder()
df['country_encoded'] = label_encoder.fit_transform(df['country'])

column_trans = ColumnTransformer([('country_encoded', OneHotEncoder(),['country_encoded'])], remainder='passthrough')
X = df[['year', 'country_encoded']]
y = df['value']
X_transform = column_trans.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_transform, y, test_size=0.3, random_state=42)

#roc specific data 
df_roc = df.copy()

label_encoder = LabelEncoder()
df_roc['country_encoded'] = label_encoder.fit_transform(df_roc['country'])
df_roc['value'] = (df_roc['value'] > 0.5).astype(int)

column_trans = ColumnTransformer([('country_encoded', OneHotEncoder(),['country_encoded'])], remainder='passthrough')
X_roc = df_roc[['year', 'country_encoded']]
y_roc = df_roc['value']
X_roc_transform = column_trans.fit_transform(X_roc)
X_roc_train, X_roc_test, y_roc_train, y_roc_test = train_test_split(X_roc_transform, y_roc, test_size=0.3, random_state=42)



# Isimti saliu duplikatus
df_unique_countries = df.drop_duplicates(subset=['country', 'country_encoded'])
# Lietuva - default
default_country_code = df_unique_countries[df_unique_countries['country'] == 'Lithuania']['country_encoded'].iloc[0]
dropdown_options = [{'label': country, 'value': code} for country, code in zip(df_unique_countries['country'], df_unique_countries['country_encoded'])]


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='country-dropdown',
        options=dropdown_options,
        value=default_country_code,  # Defaultas - Lithuania
        searchable=False,
        clearable=False
    ),
    dcc.Graph(id='health-index-graph'),
    html.Div([
        html.Label('Select number of clusters (1-10):'),
        dcc.Dropdown(
            id='cluster-dropdown',
            options=[{'label': i, 'value': i} for i in range(1, 11)],
            value=3,  # Defaultas - 3 clusteriai
            clearable=False
        ),
    ]),
    dcc.Graph(id='elbow-graph'),
    dcc.Graph(id='kmeans-graph'),
    dcc.Graph(id='random_forest'),
    dcc.Graph(id='plot_roc_curve'),
    html.Div(id='roc_auc_text')
    
])

@app.callback(
    Output('health-index-graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_health_index_graph(selected_country):
    df_country = df[df['country_encoded'] == selected_country]
    df_country = df_country.sort_values('year')

    X = df_country[['year', 'country_encoded']]
    y = df_country['value']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    df_country['predicted_value'] = model.predict(X)

    trace_real = go.Scatter(x=df_country['year'], y=df_country['value'], mode='markers', name='Real Values', marker=dict(size=10))
    trace_pred = go.Scatter(x=df_country['year'], y=df_country['predicted_value'], mode='markers', name='Model Predictions', marker=dict(size=10))

    fig = go.Figure()
    fig.add_trace(trace_real)
    fig.add_trace(trace_pred)
    fig.update_layout(title=f'Health Index Over Years - {df_country.iloc[0]["country"]}', xaxis_title='Year', yaxis_title='Value')

    return fig

@app.callback(
    Output('kmeans-graph', 'figure'),
    [Input('cluster-dropdown', 'value')]
)
def update_kmeans_graph(n_clusters):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[['country_encoded', 'value']]) 
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X_scaled)
    clusters = kmeans.labels_

    trace_kmeans = go.Scatter(
        x=X_scaled[:, 0],
        y=X_scaled[:, 1],
        mode='markers',
        marker=dict(color=clusters, colorscale='Viridis', size=10),
        name='K-means Clustering'
    )

    layout = go.Layout(
        title=f'K-means Clustering with {n_clusters} Clusters',
        xaxis=dict(title='Country (Standardized)'),
        yaxis=dict(title='Value (Standardized)'),
        coloraxis=dict(colorbar=dict(title='Cluster'))
    )


    fig = go.Figure(data=[trace_kmeans], layout=layout)
    return fig

@app.callback(
Output('elbow-graph', 'figure'),
[Input('cluster-dropdown', 'value')]

)
def elbow_graph(dummy):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[['country_encoded', 'value']]) 
    
    inertia = []
    for k in range(1, 11):  
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        inertia.append(kmeans.inertia_)

    trace_elbow = go.Scatter(
        x=list(range(1, 11)),
        y=inertia,
        mode='lines+markers',
        name='Sum of Squared Distances',
        marker=dict(color='blue')
    )
    layout = go.Layout(
        title='Elbow Graph for K-means Clustering',
        xaxis=dict(title='Number of Clusters'),
        yaxis=dict(title='Sum of Squared Distances')
    )
    fig = go.Figure(data=[trace_elbow], layout=layout)
    return fig

@app.callback(
Output('random_forest', 'figure'),
[Input('cluster-dropdown', 'value')]
)

def random_forest(dummy):
    X = df[['country_encoded', 'year']]
    y = df['value']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    clf = RandomForestRegressor(random_state=42)
    clf.fit(X_train, y_train)

    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]

    trace = go.Bar(
        x=importances[indices],
        y=X_train.columns[indices],
        orientation='h',
        marker=dict(
            color='rgba(50, 171, 96, 0.6)',  
            line=dict(color='rgba(50, 171, 96, 1.0)', width=1)
        )
    )

    layout = go.Layout(
        title='Importance of year and country to health quality',
        xaxis=dict(title='Importance'),
        yaxis=dict(title='Feature'),
        margin=dict(l=150),  
        showlegend=False
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig


@app.callback(
    Output('plot_roc_curve', 'figure'),
    [Input('plot_roc_curve', 'id')]
)
def update_roc_curve(dummy):
    clf = LogisticRegression(random_state=42, max_iter=1000)
    clf.fit(X_roc_train, y_roc_train)  # Use the training data from the separate DataFrame

    y_scores = clf.predict_proba(X_roc_test)[:, 1]  # Use the test data from the separate DataFrame
    fpr, tpr, thresholds = roc_curve(y_roc_test, y_scores)
    roc_auc = auc(fpr, tpr)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name=f'ROC Curve (AUC = {roc_auc:.2f})'))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash'), name='Random Guess'))
    fig.update_layout(title='ROC Curve',
                      xaxis_title='False Positive Rate',
                      yaxis_title='True Positive Rate',
                      legend=dict(x=0.6, y=0.1),
                      margin=dict(l=50, r=50, t=50, b=50),
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)')
    return fig

@app.callback(
    Output('roc_auc_text', 'children'),
    [Input('plot_roc_curve', 'id')]
)
def update_auc_text(dummy):
    clf = LogisticRegression(random_state=42, max_iter=1000)
    clf.fit(X_roc_train, y_roc_train)  # Use the training data from the separate DataFrame

    y_scores = clf.predict_proba(X_roc_test)[:, 1]  # Use the test data from the separate DataFrame
    fpr, tpr, thresholds = roc_curve(y_roc_test, y_scores)
    roc_auc = auc(fpr, tpr)
    return f"AUC: {roc_auc:.2f}"

if __name__ == '__main__':
    app.run_server(debug=True)