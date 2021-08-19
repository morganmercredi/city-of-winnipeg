"""
Simple data exploration using the City of Winnipeg's "Library Incidents" dataset.

The dataset can be downloaded here: 
https://data.winnipeg.ca/Libraries/Library-Incident-Reports/ffe7-mwdv/data    
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


sns.set()

# Read in the file
incidents = pd.read_csv('Library_Incident_Reports.csv')

# Clean up the table, set the date column as the index
incidents = incidents.drop(columns='ID')
incidents = incidents.set_index('Date')
incidents.index = pd.to_datetime(incidents.index)

# Sort the number of incidents by library
by_library = incidents.groupby('Location').size().sort_values(ascending=False)

# Show the incidents for each library
plt.figure()
by_library.sort_values(ascending=True).plot(kind='barh')
plt.gca().set_xlabel('Number of incidents')
plt.gca().set_ylabel('Library')
plt.gca().set_title('Reported Incidents by Library')

# Group incidents by seriousness
print(incidents.groupby('Serious').size())

# Show only serious incidents
# For now, the x-axis shows fractional ticks (2.5, 7.5, etc)
plt.figure()
incidents[incidents.Serious == 'Yes'].groupby('Type').size().sort_values().plot(kind='barh')
plt.gca().set_xlabel('Number of incidents')
plt.gca().set_ylabel('Incident type')
plt.gca().set_title('Distribution of Serious Incidents')

# Sort incidents by type
by_type = incidents.groupby('Type').size().sort_values(ascending=False)

# Get the number of incidents by year
by_year = incidents.groupby(incidents.index.year).size()

# Show the number of incidents each year
plt.figure()
by_year.plot(kind='bar')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of incidents')
plt.gca().set_title('Yearly Library Incidents')

# Show the incidents for the year 2012
print(incidents.loc['2012']) # there are only two incidents recorded

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

# Get the daily number of daily incidents
daily_incidents = incidents.resample('D', kind='period').size()

# Get the number of incidents by year and type
by_year_and_type = incidents.pivot_table(index=incidents.index.year,
                                         columns='Type',
                                         aggfunc='size').fillna(0)

# Get the number of incidents by year and library
by_year_and_library = incidents.pivot_table(index=incidents.index.year,
                                            columns='Location',
                                            aggfunc='size').fillna(0)

# Get the number of incidents by year, library, and type
by_year_library_type = incidents.pivot_table(index=incidents.index.year,
                                             columns=['Location', 'Type'],
                                             aggfunc='size').fillna(0)

plt.show()

