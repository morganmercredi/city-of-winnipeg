"""
Data exploration using the City of Winnipeg's "Transit Pass-ups" dataset
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely import wkt

sns.set()

# Path to file
file_path = '../../Sample Data Sets/Transit_Pass-ups.csv'

# Read the file
passups = pd.read_csv(file_path)

# Convert times to datetimes
passups['Time'] = pd.to_datetime(passups['Time'])

# Show number of pass-up types
print(passups.groupby('Pass-Up Type').size())

# Get number of passups per month
by_month = passups.groupby(passups.Time.dt.month).size()

# Plot the monthly figures
plt.figure()
by_month.plot(kind='bar')
plt.gca().set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                    'Sep', 'Oct', 'Nov', 'Dec'])
plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Total Monthly Pass-ups')

# Get number of passups per year
by_year = passups.groupby(passups.Time.dt.year).size()

# Plot the yearly figures
plt.figure()
by_year.plot(kind='bar')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Total Yearly Pass-ups')

# Show number of passups by day of week
by_day = passups.groupby(passups.Time.dt.dayofweek).size()

# Plot the daily figures
plt.figure()
by_day.plot(kind='bar')
plt.gca().set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])
plt.gca().set_xlabel('Day of week')
plt.gca().set_ylabel('Number of Pass-ups')
plt.gca().set_title('Total Daily Pass-ups')

# Get the number of passups per day
daily_passups = passups.set_index('Time').resample('D', kind='period').size()

# Plot the daily passups
plt.figure()
daily_passups.plot()
plt.gca().set_xlabel('Date')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Total Daily Pass-ups')

# Resample and plot weekly passups
plt.figure()
daily_passups.resample('W', kind='period').sum().plot()
plt.gca().set_xlabel('Date')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Total Weekly Pass-ups')

# Create a 7-day rolling average for total daily passups
plt.figure()
daily_passups.rolling(7, center=True).mean().plot()
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_xlabel('Date')
plt.gca().set_title('7-day Rolling Average of Transit Pass-Ups')

# Create a 7-day rolling average for total daily passups in 2015 only
plt.figure()
daily_passups.rolling(7, center=True).mean().loc['2015'].plot()
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_xlabel('Date')
plt.gca().set_title('7-day Rolling Average of Transit Pass-Ups (2015)')

# Get wheelchair passups only
wheelchair_passups = passups[passups['Pass-Up Type'] == 'Wheelchair User Pass-Up']

# Show number of wheelchair passups per month
wheelchair_by_month = wheelchair_passups.groupby(passups.Time.dt.month).size()

# Plot the monthly figures
plt.figure()
wheelchair_by_month.plot(kind='bar')
plt.gca().set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                    'Sep', 'Oct', 'Nov', 'Dec'])
plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Monthly Wheelchair Pass-ups')

# Show number of passups per year
wheelchair_by_year = wheelchair_passups.groupby(passups.Time.dt.year).size()

# Plot the yearly figures
plt.figure()
wheelchair_by_year.plot(kind='bar')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Yearly Wheelchair Pass-ups')

# Show number of passups by day of week
wheelchair_by_day = wheelchair_passups.groupby(passups.Time.dt.dayofweek).size()

# Plot the daily figures
plt.figure()
wheelchair_by_day.plot(kind='bar')
plt.gca().set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])
plt.gca().set_xlabel('Day of week')
plt.gca().set_ylabel('Number of Pass-ups')
plt.gca().set_title('Total Daily Wheelchair Pass-ups')

# Get the number of wheelchair passups per day
daily_wheelchair_passups = wheelchair_passups.set_index('Time').resample('D', kind='period').size()

# Plot the daily wheelchair passups
plt.figure()
daily_wheelchair_passups.plot()
plt.gca().set_xlabel('Date')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Total Daily Wheelchair Pass-ups')

# Resample and plot weekly wheelchair passups
plt.figure()
daily_wheelchair_passups.resample('W', kind='period').sum().plot()
plt.gca().set_xlabel('Date')
plt.gca().set_ylabel('Number of pass-ups')
plt.gca().set_title('Total Weekly Wheelchair Pass-ups')

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

# Check for missing values
print(passups.isna().sum()) 

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

# Add the latitude and longitude for a closer look
gdf['Longitude'] = pd.Series(dtype=float)
gdf['Latitude'] = pd.Series(dtype=float)

# Go through the coordinates and extract the latitude and longitude
for (index, loc) in enumerate(gdf.Location):
    if loc is not None:
        gdf['Longitude'].iloc[index] = loc.x
        gdf['Latitude'].iloc[index] = loc.y
    else:
        gdf['Longitude'].iloc[index] = None
        gdf['Latitude'].iloc[index] = None

# For simplicity, just remove all missing values
# This could have been done earlier too
gdf = gdf.dropna()

# There are a few zero latitude values. Get rid of them.
gdf = gdf[gdf['Latitude'] != 0]

plt.show()