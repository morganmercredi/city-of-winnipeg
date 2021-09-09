"""
Simple data exploration using the City of Winnipeg's "Library Incidents" dataset.

The dataset can be downloaded here: 
https://data.winnipeg.ca/Libraries/Library-Incident-Reports/ffe7-mwdv/data    
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as datetime


sns.set()

file_path = '../../Sample Data Sets/Library_Incident_Reports.csv'

# Read in the csv file
incidents = pd.read_csv(file_path)

# Clean up the table, set the date column as the index
incidents = incidents.drop(columns='ID')
incidents = incidents.set_index('Date')
incidents.index = pd.to_datetime(incidents.index)

# Get the earliest recorded incident for each library
print(incidents.groupby('Location').apply(lambda x: x.index.min()).sort_values())

# Sort the number of incidents by library
by_library = incidents.groupby('Location').size().sort_values(ascending=False)

# Show the number of incidents for each library
plt.figure()
by_library.sort_values(ascending=True).plot(kind='barh')
plt.gca().set_xlabel('Number of incidents')
plt.gca().set_ylabel('Library')
plt.gca().set_title('Reported Library Incidents (2012 - 2021)')

# Group incidents by seriousness
print(incidents.groupby('Serious').size())

# Show only serious incidents
plt.figure()
incidents[incidents.Serious == 'Yes'].groupby('Type').size().sort_values().plot(kind='barh')
plt.gca().set_xlabel('Number of incidents')
plt.gca().set_ylabel('Incident type')
plt.gca().set_title('Serious Library Incidents (2012 - 2021)')
plt.gca().set_xticks(range(0, 25, 5))

# Sort incidents by type
by_type = incidents.groupby('Type').size().sort_values()

# Show total incidents by type
plt.figure()
by_type.plot(kind='barh')
plt.gca().set_xlabel('Number of incidents')
plt.gca().set_ylabel('Incident type')
plt.gca().set_title('Reported Library Incidents (2012 - 2021)')

# Get the number of incidents by year
by_year = incidents.groupby(incidents.index.year).size()

# Show the number of incidents each year
plt.figure()
by_year.plot(kind='bar')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Total Yearly Library Incidents')

# Show the incidents for the year 2012
print(incidents.loc['2012']) # there are only two incidents recorded

# Get the number of incidents by month
by_month = incidents.groupby(incidents.index.month).size()

# Show the number of incidents each month
plt.figure()
by_month.plot(kind='bar')
plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Total Library Incidents by Month')
plt.gca().set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 
                           'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Get the number of incidents by day of week
by_day_of_week = incidents.groupby(incidents.index.dayofweek).size()

# Show the number of incidents each day of the week
plt.figure()
by_day_of_week.plot(kind='bar')
plt.gca().set_xlabel('Day of week')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Total Library Incidents by Day of Week')
plt.gca().set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])

# Get the number of incidents by year and type
by_year_and_type = incidents.pivot_table(index=incidents.index.year,
                                         columns='Type',
                                         aggfunc='size').fillna(0)

# Pick a few types of incidents and show how they've varied over the years
plt.figure()
by_year_and_type[['Inappropriate Behaviour', 'Intoxication', 'Assault']].plot(kind='bar').legend(loc='best')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Reported Library Incidents Over Time')

# Get the number of incidents by year and library
by_year_and_library = incidents.pivot_table(index=incidents.index.year,
                                            columns='Location',
                                            aggfunc='size').fillna(0)

# Pick a few libraries and show how incidents varied over the years
plt.figure()
by_year_and_library[['St. Vital', 'Louis Riel', 'Cornish']].plot(kind='bar').legend(loc='upper left')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Reported Library Incidents Over Time')

# Get the number of incidents by year, library, and type
by_year_library_type = incidents.pivot_table(index=incidents.index.year,
                                             columns=['Location', 'Type'],
                                             aggfunc='size').fillna(0)

# Get the daily number of daily incidents
daily_incidents = incidents.resample('D', kind='period').size()

# The date that Millennium library implemented enhanced security screening
millennium_screening = pd.to_datetime('2019-02-27')

# The date that libraries first shut down due to COVID-19
first_lockdown = pd.to_datetime('2020-03-16')

# Get the daily number of daily incidents at the Millennium library
daily_millennium_incidents = incidents[incidents['Location'] == 'Millennium'].resample('D', kind='period').size()

# Resample to weekly incidents and show them for 2018 and 2019
fig, ax = plt.subplots(2, figsize=(10, 10))
daily_millennium_incidents.resample('W', kind='period').sum()['2018'].plot(ax=ax[0])
daily_millennium_incidents.resample('W', kind='period').sum()['2019'].plot(ax=ax[1]) 
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

# Alternatively, view the total weekly incidents on a single chart
fig = plt.figure(figsize=(10, 5))
ax = daily_millennium_incidents.resample('W', kind='period').sum()['2017':'2019'].plot()
ax.set_ylabel('Number of incidents')
ax.set_ylim([0, 25]) 
ax.set_title('Weekly Incidents at Millennium Library (2017 - 2019)')
plt.axvline(x=millennium_screening, linestyle='--', color='r'); 
plt.annotate(xytext=(millennium_screening + datetime.timedelta(days=10), 20), 
             xy=(millennium_screening, 15.5),
             text='enhanced screening begins',
             arrowprops=dict(color='red', arrowstyle='->'),
             bbox=dict(pad=5, facecolor="none", edgecolor="none"))

plt.show()

