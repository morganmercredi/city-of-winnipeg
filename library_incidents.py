"""
Simple data exploration using the City of Winnipeg's "Library Incidents" dataset.

The dataset can be downloaded here: 
https://data.winnipeg.ca/Libraries/Library-Incident-Reports/ffe7-mwdv/data    
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as datetime


sns.set()

# Link to the csv with library incident data
url = 'https://data.winnipeg.ca/api/views/ffe7-mwdv/rows.csv?accessType=DOWNLOAD'

# Download and read the csv using pandas
incidents = pd.read_csv(url)

# Clean up the table, set the date column as the index
incidents = incidents.drop(columns='ID')
incidents = incidents.set_index('Date')
incidents.index = pd.to_datetime(incidents.index)

# Rename 'Other' incidents as 'Uncategorized'
incidents['Type'] = incidents['Type'].str.replace('Other', 'Uncategorized')

# Get the earliest recorded incident for each library
print(incidents.groupby('Location').apply(lambda x: x.index.min()).sort_values())

# Sort the number of incidents by library
by_library = incidents.groupby('Location').size().sort_values(ascending=False)

# Show the number of incidents for each library
plt.figure()
by_library.sort_values(ascending=True).plot(kind='barh')
plt.gca().set_xlabel('Number of incidents')
plt.gca().set_ylabel('Library')
plt.gca().set_title('Reported Library Incidents Since 2012')

# Group incidents by seriousness
print(incidents.groupby('Serious').size())

# Show only serious incidents
plt.figure()
incidents[incidents.Serious == 'Yes'].groupby('Type').size().sort_values().plot(kind='barh')
plt.gca().set_xlabel('Number of incidents')
plt.gca().set_ylabel('Incident type')
plt.gca().set_title('Library Incidents Listed as "Serious" Since 2012')
plt.gca().set_xticks(range(0, 25, 5))

# Sort incidents by type
by_type = incidents.groupby('Type').size().sort_values()

# Show total incidents by type
plt.figure()
by_type.plot(kind='barh')
plt.gca().set_xlabel('Number of incidents')
plt.gca().set_ylabel('Incident type')
plt.gca().set_title('Library Incidents Since 2012')

# Get the number of incidents by year
by_year = incidents.groupby(incidents.index.year).size()

# Show the incidents for the year 2012
print(incidents.loc['2012']) # there are only two incidents recorded

# Remove the year 2012 just to make things simpler (incomplete data)
incidents = incidents.sort_index().loc['2013':'2021'] # sorted to avoid deprecation warning

# Show the number of incidents each year
plt.figure()
by_year.loc['2013':'2021'].plot(kind='bar')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Yearly Library Incidents') 

# Get the number of incidents by month
by_month = incidents.groupby(incidents.index.month).size()

# Show the number of incidents each month
plt.figure()
by_month.plot(kind='bar')
plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Library Incidents by Month')
plt.gca().set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 
                           'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Get the number of incidents by day of week
by_day_of_week = incidents.groupby(incidents.index.dayofweek).size()

# Show the number of incidents each day of the week
plt.figure()
by_day_of_week.plot(kind='bar')
plt.gca().set_xlabel('Day of week')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Library Incidents by Day of Week')
plt.gca().set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])

# Get the number of incidents by time of day
by_time = incidents.groupby(incidents.index.time).size()

# Show the incidents by time of occurrence
plt.figure()
hourly_ticks = 4*60*60*np.arange(6)
by_time.plot(xticks=hourly_ticks)
plt.gca().set_xlim([0, 4*60*60*6])
plt.gca().set_xlabel('Time of Day')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Library Incidents by Time of Occurrence')

# Even better, group the incidents by hour of day
by_hour = incidents.groupby(incidents.index.hour).size()

# Show the hourly figures
plt.figure()
by_hour.plot()
plt.gca().set_xticks([0, 4, 8, 12, 16, 20])
plt.gca().set_xlim([0, 23])
plt.gca().set_xticklabels(['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'])
plt.gca().set_xlabel('Time of day')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Hourly Library Incidents')

# Get the most common incident reported at each library
most_common_incidents = incidents.groupby(['Location']).apply(lambda x: x.groupby('Type').size().idxmax())
print(most_common_incidents)

# Get the most common incident reported at each library each year
# First, group the incidents by location and year
grouped = incidents.groupby(['Location', incidents.index.year])

# Next, for each group, find the number of incidents in each category
# and find the type with the highest occurrence
most_common_incidents_by_year = grouped.apply(lambda x: x.groupby('Type').size().idxmax())

# Unstack for ease of viewing
most_common_incidents_by_year = most_common_incidents_by_year.unstack(level=0).fillna('-')

# Show the most common incidents per year at Millennium library
print(most_common_incidents_by_year['Millennium'])

# Get the number of incidents by year and type
by_year_and_type = incidents.pivot_table(index=incidents.index.year,
                                         columns='Type',
                                         aggfunc='size').fillna(0)

# Pick a few types of incidents and show how they've varied over the years
incident_list = ['Inappropriate Behaviour', 'Intoxication', 'Assault']

plt.figure()
by_year_and_type[incident_list].plot(kind='bar').legend(loc='best', title='Incident Type')
plt.gca().set_ylim([0, 300])
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Library Incidents Over Time')

# Get the number of incidents by year and library
by_year_and_library = incidents.pivot_table(index=incidents.index.year,
                                            columns='Location',
                                            aggfunc='size').fillna(0)

# Pick a few libraries and show how incidents varied over the years
library_list = ['St. Vital', 'Louis Riel', 'Cornish']

plt.figure()
by_year_and_library[library_list].plot(kind='bar').legend(loc='upper left', title='Library')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Library Incidents Over Time')

# Get the number of incidents by year, library, and type
by_year_library_type = incidents.pivot_table(index=incidents.index.year,
                                             columns=['Location', 'Type'],
                                             aggfunc='size').fillna(0)

# For Millennium library, pick a few types of incidents, and show how they've varied over time
incident_list = ['Inappropriate Behaviour', 'Intoxication', 'Uncategorized']

plt.figure()
by_year_library_type['Millennium'][incident_list].plot(kind='bar').legend(loc='upper left', title='Incident Type')
plt.gca().set_ylim([0, 300])
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Library Incidents Over Time (Millennium Library)')

# NOTE: by_year_and_type = by_year_library_type.groupby(axis=1, level=1).sum()
# by_year_and_library = by_year_library_type.groupby(axis=1, level=0).sum() 

# Get the daily number of daily incidents
daily_incidents = incidents.resample('D').size()

# The date that Millennium library implemented enhanced security screening
millennium_screening = pd.to_datetime('2019-02-27')

# The date that libraries first shut down due to COVID-19
first_lockdown = pd.to_datetime('2020-03-16')

# Get the daily number of daily incidents at the Millennium library
daily_millennium_incidents = incidents[incidents['Location'] == 'Millennium'].resample('D').size()

# Resample to weekly incidents and show them for 2018 and 2019
fig, ax = plt.subplots(2, figsize=(10, 10))
daily_millennium_incidents.resample('W').sum().loc['2018'].plot(ax=ax[0])
daily_millennium_incidents.resample('W').sum().loc['2019'].plot(ax=ax[1]) 
ax[0].set_ylabel('Number of incidents')
ax[1].set_ylabel('Number of incidents')
ax[0].set_ylim([0, 30]) 
ax[1].set_ylim([0, 30])
ax[0].set_title('Weekly Incidents at Millennium Library in 2018 and 2019')
plt.axvline(x=millennium_screening, linestyle='--', color='r'); 
plt.annotate(xytext=(millennium_screening + datetime.timedelta(days=10), 25), 
             xy=(millennium_screening, 22.5),
             text='enhanced screening begins',
             arrowprops=dict(color='red', arrowstyle='->'),
             bbox=dict(pad=5, facecolor="none", edgecolor="none"))

# Alternatively, view the total weekly incidents for 2018 and 2019 on a single chart
fig = plt.figure(figsize=(10, 5))
ax = daily_millennium_incidents.resample('W', kind='period').sum()['2017':'2019'].plot()
ax.set_ylabel('Number of incidents')
ax.set_ylim([0, 25]) 
ax.set_title('Total Weekly Incidents at Millennium Library')
plt.axvline(x=millennium_screening, linestyle='--', color='r'); 
plt.annotate(xytext=(millennium_screening + datetime.timedelta(days=20), 20), 
             xy=(millennium_screening, 15.5),
             text='enhanced screening begins',
             arrowprops=dict(color='red', arrowstyle='->'),
             bbox=dict(pad=5, facecolor="none", edgecolor="none"))

# Show the total weekly incidents going from 2013 to 2021
fig = plt.figure(figsize=(30, 5))
ax = daily_millennium_incidents.resample('W').sum().loc['2013':'2021'].plot()
ax.set_ylabel('Number of incidents')
ax.set_ylim([0, 25]) 
ax.set_title('Weekly Incidents at Millennium Library')
plt.axvline(x=millennium_screening, linestyle='--', color='r'); 
plt.annotate(xytext=(millennium_screening + datetime.timedelta(days=20), 20), 
             xy=(millennium_screening, 15.5),
             text='enhanced screening \nbegins',
             arrowprops=dict(color='red', arrowstyle='->'),
             bbox=dict(pad=5, facecolor="none", edgecolor="none"))
plt.axvline(x=first_lockdown, linestyle='--', color='r'); 
plt.annotate(xytext=(first_lockdown + datetime.timedelta(days=15), 15), 
             xy=(first_lockdown, 12.5),
             text='COVID-19 pandemic \nbegins',
             arrowprops=dict(color='red', arrowstyle='->'),
             bbox=dict(pad=5, facecolor="none", edgecolor="none"))

plt.show()

