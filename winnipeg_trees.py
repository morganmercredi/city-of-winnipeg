"""
Simple data exploration using the City of Winnipeg's "Tree Inventory" dataset.

The dataset can be downloaded here:
https://data.winnipeg.ca/Parks/Tree-Inventory-Map/xyma-gm38
"""
import numpy as np
import pandas as pd
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt


url = 'https://data.winnipeg.ca/api/views/h923-dxid/rows.csv?accessType=DOWNLOAD'

# Load the trees dataset
trees = pd.read_csv(url)

# Remove the 'x', 'y', and 'ded_tag_no' columns
trees.drop(columns=['x', 'y', 'ded_tag_no'], inplace=True)

# Get the number of trees per ward, sorted
trees_by_ward = trees.groupby('ward').size().sort_values(ascending=False)

# Get the number of trees per neighbourhood, sorted
trees_by_neighbourhood = trees.groupby('nbhd').size().sort_values(ascending=False)

def get_most_treed_nbhds(group, n=5):
    """Get the n-most treed neighbourhoods in a group."""
    top_trees = group.groupby('nbhd').size().sort_values(ascending=False)[:n]
    return top_trees

# Get neighbourhoods with the most trees in each ward
most_treed_neighbourhoods = trees.groupby('ward').apply(get_most_treed_nbhds)

def get_most_common_trees(group, n=5):
    """Get the top n tree species in a group."""
    top_trees = group.groupby('common').size().sort_values(ascending=False)[:n]
    return top_trees

# Get most common tree type by ward
most_common_trees_by_ward = trees.groupby('ward').apply(get_most_common_trees)

# Get most common tree type by ward and neighbourhood
most_common_trees_by_ward_neighbourhood = trees.groupby(['ward', 'nbhd']).apply(get_most_common_trees)

# Sort tree species by average diameter
tree_species_by_mean_diameter = trees.groupby('common')['dbh'].mean().sort_values(ascending=False)

# Sort tree species by standard deviation in diameter
tree_species_by_stddev = trees.groupby('common')['dbh'].std().sort_values(ascending=False)

# Show statistics for each tree species
tree_species_stats = trees.groupby('common')['dbh'].agg(['mean', 'std'])

# Show the relationship between mean measured diameter and standard deviation
# in measured diameter
plt.figure()
tree_species_stats.plot.scatter(x='mean', y='std', c='b')
plt.gca().set_xlabel('Mean measured diameter')
plt.gca().set_ylabel('Standard deviation in measured diameter')
plt.gca().set_title('Mean and Standard Deviation in Measured Diameter by Tree Species')

# Show the distribution of diameters for American Elm (e.g.)
plt.figure()
trees[trees['common'] == 'American Elm']['dbh'].hist(bins=100, range=(0, 125))
plt.gca().set_xlabel('Diameter')
plt.gca().set_ylabel('Number of occurrences')
plt.gca().set_title('Distribution of American Elm Diameters')

# Here, I try to extract latitudes and longitues from the point column
# This was before I found the Shapely and Geopandas packages
def get_lat_lon(geom):
    """Extract latitude and longitude from geometry column"""
    geom = geom.split()
    lat = float(geom[2].rstrip(')'))
    lon = float(geom[1].lstrip('('))
    return lat, lon

# Extract the latitudes and longitudes from the geometry column
# This is a series of tuples
lat_lon = trees['the_geom'].apply(get_lat_lon)

# Split the tuples into separate columns in the tree table
trees[['lat', 'lon']] = lat_lon.to_list()

# Use kernel density estimation on the tree locations
# Do a grid search over a few different bandwidths (this takes an hour of my PC)
bandwidths = [0.0001, 0.0005, 0.001]
grid = GridSearchCV(KernelDensity(kernel='gaussian'), {'bandwidth': bandwidths},
                    cv=3, n_jobs=-1)
grid.fit(np.array(trees[['lon', 'lat']]));
print(grid.best_params_) # 0.0005 is the best choice

# Choose the best model
model = grid.best_estimator_

# Create a set of points to predict the density
x = np.linspace(-96.95, -97.35, 200)
y = np.linspace(49.7, 49.98, 200)
xx, yy = np.meshgrid(x, y)

# Get a set of density predictions
log_pred = model.score_samples(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
pred = np.exp(log_pred)

# Show the tree distribution
levels = np.linspace(pred.min(), pred.max(), 100)
plt.contourf(xx, yy, pred, alpha=0.3, levels=levels)

plt.show()