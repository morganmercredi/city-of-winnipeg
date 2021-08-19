"""
Simple data exploration using the City of Winnipeg's "Transit Pass-ups" dataset.

The dataset can be downloaded here: 
https://data.winnipeg.ca/Transit/Transit-Pass-ups/mer2-irmb/data
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely import wkt


sns.set()

# Path to file (for me)
file_path = '../../Sample Data Sets/Transit_Pass-ups.csv'

# Read the file
passups = pd.read_csv(file_path)

# Convert times to datetimes
passups['Time'] = pd.to_datetime(passups['Time'])

# Show number of pass-up types
print(passups.groupby('Pass-Up Type').size())

# Show number of passups per month
by_month = passups.groupby(passups.Time.dt.month).size()

# Plot the monthly figures
plt.figure()
by_month.plot(kind='bar')
plt.gca().set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                    'Sep', 'Oct', 'Nov', 'Dec'])
plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Number of passups')
plt.gca().set_title('Monthly Passups')

# Show number of passups per year
by_year = passups.groupby(passups.Time.dt.year).size()

# Plot the yearly figures
plt.figure()
by_year.plot(kind='bar')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of passups')
plt.gca().set_title('Yearly Passups')

# Show number of passups by day of week
by_day = passups.groupby(passups.Time.dt.dayofweek).size()

# Plot the daily figures
plt.figure()
by_day.plot(kind='bar')
plt.gca().set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])
plt.gca().set_xlabel('Day of week')
plt.gca().set_ylabel('Number of Passups')
plt.gca().set_title('Daily Passups')

# Get the number of passups per day
daily_passups = passups.set_index('Time').resample('D', kind='period').size()

# Plot the daily passups
plt.figure()
daily_passups.plot()
plt.gca().set_xlabel('Date')
plt.gca().set_ylabel('Number of passups')
plt.gca().set_title('Daily Passups')

# Resample and plot weekly passups
plt.figure()
daily_passups.resample('W', kind='period').sum().plot()
plt.gca().set_xlabel('Date')
plt.gca().set_ylabel('Number of passups')
plt.gca().set_title('Weekly Passups')

# Create a 30-day rolling average for total daily passups
daily_passups.rolling(30, center=True).mean().plot()
plt.gca().set_ylabel('Count')

# Convert the GPS data to shapely objects
# Check if the GPS data is valid 
def wkt_loads(x):
    try:
        return wkt.loads(x)
    except Exception:
        return None

passups['Location'] = passups['Location'].apply(wkt_loads)

# Get a separate table with passups from a full bus
full_passups = passups[passups['Pass-Up Type'] == 'Full Bus Pass-Up']

plt.show()