# DBSCAN clustering

import pandas as pd, numpy as np, matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint

dataset = pd.read_csv('complete_cleaned_duplicates_removed_data.csv', encoding = "ISO-8859-1")
df = dataset[['lat', 'lng']]
coords = df.as_matrix(columns=['lat', 'lng'])

kms_per_radian = 6371.0088
epsilon = 1.5 / kms_per_radian
db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
cluster_labels = db.labels_
num_clusters = len(set(cluster_labels))
clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])

# Function to find the centroid of each cluster
def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)
centermost_points = clusters.map(get_centermost_point)

# Create pandas DF of only centroids
lats, lngs = zip(*centermost_points)
rep_points = pd.DataFrame({'lng':lngs, 'lat':lats})

# Replacing all lat values in original df with the nearest centroid values
A = pd.Series(rep_points['lat'])
B = pd.Series(df['lat'])
B = pd.Series(A.values, A.values).sort_index().drop_duplicates().reindex(B.values, method='nearest')
B = B.to_frame().reset_index()
dataset['lat'] = B

# Replacing all lng values in original df with the nearest centroid values
C = pd.Series(rep_points['lng'])
D = pd.Series(df['lng'])
D = pd.Series(C.values, C.values).sort_index().drop_duplicates().reindex(D.values, method='nearest')
D = D.to_frame().reset_index()
dataset['lng'] = D
dataset.to_csv('complete_clustered_duplicates_removed_data.csv', encoding='utf-8', index=False)

# Check number of lat and lng centroids created
dataset['lat'].nunique()
dataset['lng'].nunique()


# Plotting original points against centroids
# =============================================================================
# fig, ax = plt.subplots(figsize=[10, 6])
# rs_scatter = ax.scatter(rep_points['lng'], rep_points['lat'], c='#99cc99', edgecolor='None', alpha=0.7, s=120)
# df_scatter = ax.scatter(df['lng'], df['lat'], c='k', alpha=0.9, s=3)
# ax.set_title('Full data set vs DBSCAN reduced set')
# ax.set_xlabel('Longitude')
# ax.set_ylabel('Latitude')
# ax.legend([df_scatter, rs_scatter], ['Reduced set', 'Full set'], loc='upper right')
# plt.savefig('Full data vs DBSCAN centroids.png')
# plt.show()
# =============================================================================
