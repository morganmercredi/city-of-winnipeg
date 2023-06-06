"""
Data exploration using the City of Winnipeg's "Transit Pass-ups" dataset.

The datasets can be downloaded here:
https://data.winnipeg.ca/api/views/mer2-irmb/
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely import wkt

sns.set()

# Path to transit file
url = 'https://data.winnipeg.ca/api/views/mer2-irmb/rows.csv?accessType=DOWNLOAD'

# Read the file
passups = pd.read_csv(url)

# Convert times to datetimes
passups['Time'] = pd.to_datetime(passups['Time'])

# Set the time as index
passups = passups.set_index('Time')

# Show number of pass-up types
print(passups.groupby('Pass-Up Type').size())

# Show which routes have the most pass-ups
print(passups.groupby('Route Name').size().sort_values(ascending=False)[:10])

# Analyze full bus pass-ups and wheelchair pass-ups separately
full_bus_passups = passups[passups['Pass-Up Type'] == 'Full Bus Pass-Up']

# Get pass-ups by time of day
by_time = full_bus_passups.groupby(full_bus_passups.index.time).size()

# Plot the time of day figures
plt.figure()
hourly_ticks = 4*60*60*np.arange(6)
by_time.plot(xticks=hourly_ticks)
plt.gca().set_xlabel('Time of Day')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Full Bus Pass-ups by Time of Occurrence')

# Even better, group the pass-ups by hour of day
by_hour = full_bus_passups.groupby(full_bus_passups.index.hour).size()

# Show the hourly figures
plt.figure()
by_hour.plot()
plt.gca().set_xticks([0, 4, 8, 12, 16, 20])
plt.gca().set_xlim([0, 23])
plt.gca().set_xticklabels(['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'])
plt.gca().set_xlabel('Hour of occurrence')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Full Bus Pass-ups by Hour')

# Get number of passups per month
by_month = full_bus_passups.groupby(full_bus_passups.index.month).size()

# Plot the monthly figures
plt.figure()
by_month.plot(kind='bar')
plt.gca().set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                    'Sep', 'Oct', 'Nov', 'Dec'])
plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Full Bus Pass-ups by Month')

# Get number of passups per year
by_year = full_bus_passups.groupby(full_bus_passups.index.year).size()

# Plot the yearly figures
plt.figure()
by_year.plot(kind='bar')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Yearly Full Bus Pass-ups')

# Show number of passups by day of week
by_day = full_bus_passups.groupby(full_bus_passups.index.dayofweek).size()

# Plot the daily figures
plt.figure()
by_day.plot(kind='bar')
plt.gca().set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])
plt.gca().set_xlabel('Day of week')
plt.gca().set_ylabel('Number of Pass-ups')
plt.gca().set_title('Full Bus Pass-ups by Day of Week')

# Get the number of passups per day
daily_passups = full_bus_passups.resample('D').size()

# Plot the daily passups
plt.figure()
daily_passups.plot()
plt.gca().set_xlabel('Date')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Daily Full Bus Pass-ups')

# Resample and plot weekly passups
plt.figure()
daily_passups.resample('W', kind='period').sum().plot()
plt.gca().set_xlabel('Date')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Weekly Full Bus Pass-ups')

# Create a 7-day rolling average for total daily passups
plt.figure()
daily_passups.rolling(7, center=True).mean().plot()
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_xlabel('Date')
plt.gca().set_title('7-day Rolling Average of Full Bus Pass-Ups')

# Create a 7-day rolling average for total daily passups in 2015 only
plt.figure()
daily_passups.rolling(7, center=True).mean().loc['2015'].plot()
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_xlabel('Date')
plt.gca().set_title('7-day Rolling Average of Full Bus Pass-Ups (2015)')

# Get wheelchair passups only
# Repeat the above analyses for wheelchair passups only
wheelchair_passups = passups[passups['Pass-Up Type'] == 'Wheelchair User Pass-Up']

# Show number of wheelchair passups per month
wheelchair_by_month = wheelchair_passups.groupby(wheelchair_passups.index.month).size()

# Plot the monthly figures
plt.figure()
wheelchair_by_month.plot(kind='bar')
plt.gca().set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                    'Sep', 'Oct', 'Nov', 'Dec'])
plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Wheelchair Pass-ups by Month')

# Show number of passups per year
wheelchair_by_year = wheelchair_passups.groupby(wheelchair_passups.index.year).size()

# Plot the yearly figures
plt.figure()
wheelchair_by_year.plot(kind='bar')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Yearly Wheelchair Pass-ups')

# Show number of passups by day of week
wheelchair_by_day = wheelchair_passups.groupby(wheelchair_passups.index.dayofweek).size()

# Plot the daily figures
plt.figure()
wheelchair_by_day.plot(kind='bar')
plt.gca().set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])
plt.gca().set_xlabel('Day of week')
plt.gca().set_ylabel('Number of Pass-ups')
plt.gca().set_title('Wheelchair Pass-ups by Day of Week')

# Get the number of wheelchair passups per day
daily_wheelchair_passups = wheelchair_passups.resample('D').size()

# Plot the daily wheelchair passups
plt.figure()
daily_wheelchair_passups.plot()
plt.gca().set_xlabel('Date')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Daily Wheelchair Pass-ups')

# Resample and plot weekly wheelchair passups
plt.figure()
daily_wheelchair_passups.resample('W', kind='period').sum().plot()
plt.gca().set_xlabel('Date')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Weekly Wheelchair Pass-ups')

# Create a 7-day rolling average for total daily wheelchair passups
plt.figure()
daily_wheelchair_passups.rolling(7, center=True).mean().plot()
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_xlabel('Date')
plt.gca().set_title('7-day Rolling Average of Wheelchair Pass-Ups')

# Create a 7-day rolling average for total daily wheelchair passups in 2015
plt.figure()
daily_wheelchair_passups.rolling(7, center=True).mean().loc['2015'].plot()
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_xlabel('Date')
plt.gca().set_title('7-day Rolling Average of Wheelchair Pass-Ups (2015)')

# Convert the GPS data to shapely objects
# Check if the GPS data is valid first
def wkt_loads(x):
    try:
        return wkt.loads(x)
    except Exception:
        return None

passups['Location'] = passups['Location'].apply(wkt_loads)

# Load into a geopandas dataframe
gdf = gpd.GeoDataFrame(passups.copy(), geometry='Location')
gdf = gdf.set_crs('EPSG:4326')

# For simplicity, just remove all missing values
gdf = gdf.dropna()

# Let's try to eliminate points outside of Winnipeg
# Path to Winnipeg boundary file
city_map = 'https://data.winnipeg.ca/api/views/2nyq-f444/rows.csv?accessType=DOWNLOAD'

# Load the file and convert to a GeoDataFrame
wpg_borders = pd.read_csv(city_map)
wpg_borders['the_geom'] = wpg_borders['the_geom'].apply(wkt_loads)
wpg_borders = gpd.GeoDataFrame(wpg_borders.copy(), geometry='the_geom')
wpg_borders = wpg_borders.set_crs('EPSG:4326')

# Remove data points that are outside the city of Winnipeg boundary
gdf = gdf[gdf.within(wpg_borders.iloc[0]['the_geom'])]

# Show where transit pass-ups happen in Winnipeg
ax = wpg_borders.boundary.plot(edgecolor='k')
gdf.plot(markersize=0.05, ax=ax)
ax.axis('off')
ax.set_title('Winnipeg Transit Bus Pass-ups')

# Show where full bus pass-ups happen
ax = wpg_borders.boundary.plot(edgecolor='k')
gdf[gdf['Pass-Up Type'] == 'Full Bus Pass-Up'].plot(markersize=0.05, color='r', ax=ax)
ax.axis('off')
ax.set_title('Full Bus Pass-ups')

# Show where wheelchair pass-ups happen
ax = wpg_borders.boundary.plot(edgecolor='k')
gdf[gdf['Pass-Up Type'] == 'Wheelchair User Pass-Up'].plot(markersize=0.05, color='r', ax=ax)
ax.axis('off')
ax.set_title('Wheelchair User Pass-ups')

# Show both types of pass-ups on one map
ax = wpg_borders.boundary.plot(edgecolor='k', figsize=(10, 6))
gdf[gdf['Pass-Up Type'] == 'Full Bus Pass-Up'].plot(markersize=0.05, alpha=0.2, ax=ax)
gdf[gdf['Pass-Up Type'] == 'Wheelchair User Pass-Up'].plot(markersize=0.05, alpha=0.2,
                                                           color='r', ax=ax)
ax.axis('off')
for colour, label in zip(['r', 'b'], ['Wheelchair User', 'Full Bus']):
    plt.scatter([], [], c=colour, label=label)
ax.legend(frameon=False, title='Pass-up Type',
          loc='lower right', fontsize='small')
ax.set_title('Winnipeg Transit Pass-ups')

plt.show()