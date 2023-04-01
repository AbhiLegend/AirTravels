import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import streamlit as st
from sklearn.neighbors import NearestNeighbors
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors
from yellowbrick.cluster import KElbowVisualizer

# Load data
data = pd.read_csv('data_cities.csv')
# Standardize the data

# Remove non-numeric columns
# Remove non-numeric columns
data_numeric = data.drop(columns=['City', 'State'])
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_numeric)




# User interaction to select number of clusters
n_clusters = st.sidebar.slider("Select number of clusters for KMeans", 2, 10)

# Fit KMeans model
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
kmeans.fit(data_numeric)

# Add cluster labels to original DataFrame
data['kmeans_cluster'] = kmeans.labels_

from sklearn.metrics import silhouette_score
silhouette = silhouette_score(data_scaled, kmeans.labels_)
st.write('Silhouette score:', silhouette)

# Visualize results with Plotly
fig = px.scatter_3d(data, x='Internet Users (million)', y='Road Length (km)', z='Railway Route Length (km)', color='kmeans_cluster')
st.plotly_chart(fig)

# Show list of clusters with details
st.write('KMeans Clusters:')
for i in range(n_clusters):
    st.write('Cluster', i)
    st.write(data[data['kmeans_cluster'] == i].describe())
    st.write('')



# Find best cluster for new air travel routes
distances = kmeans.transform(data_numeric)
closest_cluster = np.argmin(distances, axis=1)
st.write('Best cluster for new air travel routes:', closest_cluster)

# Visualize best cluster in 3D
best_cluster = data[data['kmeans_cluster'] == closest_cluster[0]]
fig = px.scatter_3d(best_cluster, x='Internet Users (million)', y='Road Length (km)', z='Railway Route Length (km)', color='kmeans_cluster')
st.write('Best cluster visualization:')
st.plotly_chart(fig)

# Calculate centroid of best cluster
centroid = kmeans.cluster_centers_[closest_cluster[0]]
st.write('Centroid of best cluster:', centroid)

# Find cities closest to centroid
nn = NearestNeighbors(n_neighbors=5).fit(data_numeric)
distances, indices = nn.kneighbors([centroid])
closest_cities = data.iloc[indices[0],0].tolist()
st.write('Cities closest to centroid:', closest_cities)



