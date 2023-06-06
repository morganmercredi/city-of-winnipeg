"""
Simple data exploration using the City of Winnipeg's "Tree Inventory" dataset.

The dataset can be downloaded here:
https://data.winnipeg.ca/Parks/Tree-Inventory-Map/xyma-gm38
"""
import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
from shapely import wkt
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


tree_url = 'https://data.winnipeg.ca/api/views/h923-dxid/rows.csv?accessType=DOWNLOAD'
ward_url = 'https://data.winnipeg.ca/api/views/t4cg-yaxs/rows.csv?accessType=DOWNLOAD'
nbhd_url = 'https://data.winnipeg.ca/api/views/xaux-29zr/rows.csv?accessType=DOWNLOAD'

# Load the trees dataset
trees = pd.read_csv(tree_url)

# Remove the 'x', 'y', and 'ded_tag_no' columns
trees = trees.drop(columns=['x', 'y', 'ded_tag_no', 'street', 'st_from', 'st_to'])

# Load the ward boundaries
# We'll need this for calculating tree density
wards = pd.read_csv(ward_url)

# Drop some columns
wards = wards.drop(columns=['Councillor', 'Phone', 'Asst', 'AsstPhone', 'Community',
                   'Clerk', 'ClerkPhone', 'Website', 'Number'])

# Load the neighbourhood boundaries
# We'll need this for calculating tree density
nbhd = pd.read_csv(nbhd_url)

# Convert the GPS data to shapely objects
# Check if the GPS data is valid first
def wkt_loads(x):
    try:
        return wkt.loads(x)
    except Exception:
        return None

trees['the_geom'] = trees['the_geom'].apply(wkt_loads)
nbhd['the_geom'] = nbhd['the_geom'].apply(wkt_loads)
wards['the_geom'] = wards['the_geom'].apply(wkt_loads)

# Convert neighbourhood, ward, and tree inventory data to GeoDataFrames
nbhd = gpd.GeoDataFrame(nbhd.copy(), geometry='the_geom')
wards = gpd.GeoDataFrame(wards.copy(), geometry='the_geom')
trees = gpd.GeoDataFrame(trees.copy(), geometry='the_geom')

# Set the crs to latitude/longitude
nbhd = nbhd.set_crs("EPSG:4326")
wards = wards.set_crs("EPSG:4326")
trees = trees.set_crs("EPSG:4326")

# Convert to a projected crs for Manitoba (approximately)
nbhd = nbhd.to_crs('EPSG:32614')
wards = wards.to_crs('EPSG:32614')

# Get the area of the neighbourhoods and wards (in square kilometres)
wards['Area'] = wards.area/1e6
nbhd['Area'] = nbhd.area/1e6

# Get the number of trees per ward, sorted
trees_by_ward = trees.groupby('ward').size().sort_values(ascending=False)

# The wards from the tree inventory and the ward dataset match
# Merge the trees_by_ward data to the ward dataset
wards = wards.merge(trees_by_ward.rename('Number of trees'),
                            left_on='Name', right_index=True)

# Add a column for the density of trees per ward
wards['Density'] = wards['Number of trees'].div(wards['Area'])

# Plot the tree density over the ward map
plt.figure();
wards.plot('Density', legend=True, cmap='Greens');
plt.gca().set_title('Tree Density by Ward (km$^{-2}$)');
plt.axis('off');

# Get the number of trees per neighbourhood, sorted
trees_by_neighbourhood = trees.groupby('nbhd').size().sort_values(ascending=False)

# Let's check if the city neighbourhood list matches the neighbourhood list
# from the tree inventory data
# The neighbourhoods in the tree inventory are in all caps. Change to lower case.
nbhd.Name = nbhd.Name.str.lower()
trees_by_neighbourhood.index = trees_by_neighbourhood.index.str.lower()

# Get the neighbourhoods in the tree inventory that aren't in the city neighbourhood list
print(trees_by_neighbourhood[~trees_by_neighbourhood.index.isin(nbhd.Name)].index.to_list())

# Get the neighbourhoods in the city neighbourhood list that aren't in the tree inventory data
print(nbhd[~nbhd.Name.isin(trees_by_neighbourhood.index)].Name.to_list())

# So, five neighbourhoods aren't in the tree inventory dataset
# Merge the trees_by_neighbourhood data to the city neighbourhood dataset
nbhd = nbhd.merge(trees_by_neighbourhood.rename('Number of trees'),
                  left_on='Name', right_index=True)

# Add a column for the density of trees per neighbourhood
nbhd['Density'] = nbhd['Number of trees'].div(nbhd['Area'])

# Plot the tree density over the neighbourhood map
plt.figure();
nbhd.plot('Density', legend=True, cmap='Greens');
plt.gca().set_title('Tree Density by Neighbourhood (km$^{-2}$)');
plt.axis('off');

# Get the top 10 most tree dense neighbourhoods
print(nbhd.sort_values(by='Density', ascending=False)[['Name', 'Density']][:10])

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
plt.gca().set_xlabel('Mean diameter (cm)')
plt.gca().set_ylabel('Standard deviation in diameter (cm)')
plt.gca().set_title('Mean and Standard Deviation in Measured Diameter by Tree Species')

# Show the distribution of diameters for American Elm (e.g.)
plt.figure()
trees[trees['common'] == 'American Elm']['dbh'].hist(bins=100, range=(0, 125))
plt.gca().set_xlabel('Diameter (cm)')
plt.gca().set_ylabel('Number of occurrences')
plt.gca().set_title('Distribution of American Elm Diameters')

# Create separate columns for latitude and longitude
trees['Longitude'] = trees.the_geom.x
trees['Latitude'] = trees.the_geom.y

# Use kernel density estimation on the tree locations
# Do a grid search over a few different bandwidths (this takes an hour on my PC)
bandwidths = [0.0001, 0.0005, 0.001]
grid = GridSearchCV(KernelDensity(kernel='gaussian'), {'bandwidth': bandwidths},
                    cv=3, n_jobs=-1)
grid.fit(np.array(trees[['Longitude', 'Latitude']]))
print(grid.best_params_) # 0.0005 is the best choice

# Choose the best model
model = grid.best_estimator_

# Overlay the tree distribution on a city of Winnipeg boundary map
# Path to Winnipeg boundary file
city_map_url = 'https://data.winnipeg.ca/api/views/2nyq-f444/rows.csv?accessType=DOWNLOAD'

# Load the file and convert to a GeoDataFrame
wpg_borders = pd.read_csv(city_map_url)
wpg_borders['the_geom'] = wpg_borders['the_geom'].apply(wkt_loads)
wpg_borders = gpd.GeoDataFrame(wpg_borders.copy(), geometry='the_geom')
wpg_borders = wpg_borders.set_crs('EPSG:4326')

# First, plot all individual trees
ax = wpg_borders.boundary.plot(edgecolor='k')
trees.plot(markersize=0.05, color='g', ax=ax)
ax.axis('off')

# Now, plot the tree distribution
ax = wpg_borders.boundary.plot(edgecolor='k')
ax.axis('off')

# Use the limits for the city map
xmin, xmax = ax.get_xlim()
ymin, ymax = ax.get_ylim()

# Create a set of points to predict the density
x = np.linspace(xmin, xmax, 200)
y = np.linspace(ymin, ymax, 200)
xx, yy = np.meshgrid(x, y)

# Get a set of density predictions
log_pred = model.score_samples(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
pred = np.exp(log_pred)

# Show the tree distribution
levels = np.linspace(pred.min(), pred.max(), 100)
ax.contourf(xx, yy, pred, alpha=0.3, levels=levels, cmap='inferno')

plt.show()