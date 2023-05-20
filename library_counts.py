"""
Data exploration using the City of Winnipeg's "Library People Counts" dataset.

The dataset can be downloaded here: 
https://data.winnipeg.ca/Libraries/Library-People-Counts/g3zt-s3kr/data
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


sns.set()

# Link to the csv with library people count data
url = "https://data.winnipeg.ca/api/views/g3zt-s3kr/rows.csv?accessType=DOWNLOAD"

# Download and read the csv using pandas
counts = pd.read_csv(url)

# Remove the count IDs
counts = counts.drop(labels='ID', axis=1)

# Set the week as the index
counts = counts.set_index('Week End Date')

# Make the weeks into a time
counts.index = pd.to_datetime(counts.index)

# Go through the description column and separate out the library name only
counts['Library'] = [" ".join(desc.split()[:-4]) for desc in counts['Description']]

# Show the earliest recorded week for each library 
# The earliest counts start from Jan. 2009, but only in two libraries
# All libraries have started counting by December 2010
print(counts.groupby('Library').apply(lambda x: x.index.min()).sort_values())

# Let's start the count in 2011 to make things fair
counts = counts.sort_index().loc['2011':]

# Get the number of total counts per year in each library
by_library_and_year = counts.groupby(['Library', counts.index.year])['Count'].sum()
by_library_and_year = by_library_and_year.unstack(level=0).fillna(0)

# Alternatively, using pivot tables...
by_library_and_year = counts.pivot_table('Count', index=counts.index.year,
                                         columns='Library', aggfunc='sum').fillna(0)

# Get the total number of visitors to each library
by_library = by_library_and_year.sum().sort_values(ascending=True)

# Show the total number of visitors by library
plt.figure()
by_library.plot(kind='barh')
plt.gca().set_xlabel('Number of visitors (millions)')
plt.gca().set_ylabel('Library')
plt.gca().set_title('Library Visitors Since 2011')
plt.gca().set_xticks([0, 2000000, 4000000, 6000000, 8000000])
plt.gca().set_xticklabels([0, 2, 4, 6, 8])

# Group counts by year
by_year = counts.groupby(counts.index.year)['Count'].sum()

# Alternatively...
by_year = by_library_and_year.sum(axis=1)

# Show the total visitors per year
plt.figure()
by_year.plot(kind='bar')
plt.xticks(rotation = 45)
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of visitors (millions)')
plt.gca().set_title('Yearly Library Visitors')
plt.gca().set_yticks([0, 500000, 1000000, 1500000, 2000000, 2500000])
plt.gca().set_yticklabels([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])

# Show the number of visitors per year for select libraries
library_list = ['St. Boniface', 'St. Vital']

plt.figure()
by_library_and_year[library_list].plot(kind='bar')
plt.xticks(rotation = 45)
plt.gca().set_ylim([0, 130000])
plt.gca().legend(loc='best', title='Library')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of visitors')
plt.gca().set_title('Yearly Visitors for Selected Libraries')

# Get the number of visitors per month in each library
by_library_and_month = counts.pivot_table('Count', index=counts.index.month,
                                          columns='Library', aggfunc='sum').fillna(0)

# Group total visits by month
by_month = by_library_and_month.sum(axis=1)

# Show the total visitors per month
plt.figure()
by_month.plot(kind='bar')
plt.gca().set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                           'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation = 45)
plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Number of visitors (millions)')
plt.gca().set_title('Library Visitors by Month')
plt.gca().set_yticks([0, 500000, 1000000, 1500000, 2000000, 2500000])
plt.gca().set_yticklabels([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])

# Show the number of visitors each month for select libraries
library_list = ['St. Boniface', 'Cornish']

plt.figure()
by_library_and_month[library_list].plot(kind='bar')
plt.gca().set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                           'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation = 45)
plt.gca().set_ylim([0, 115000])
plt.gca().legend(loc='best', title='Library')
plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Number of visitors')
plt.gca().set_title('Library Visitors by Month for Selected Libraries')

# Get total weekly visits over time
weekly_visits = counts['Count'].resample('W').sum()

# Show total weekly visits for 2015
plt.figure()
weekly_visits.loc['2015'].plot()
plt.gca().set_xlabel('Date')
plt.gca().set_ylabel('Number of visitors')
plt.gca().set_title('Weekly Library Visitors in 2015')

# Get a new table with all counts for a given library in a week merged into one row
counts = counts.groupby([counts.index, 'Library'])
counts = counts.agg({'Count':'sum', 'Days Open':'max'}).reset_index('Library')

# Get the number of open days per year for each library
days_open = counts.pivot_table('Days Open', index=counts.index.year,
                                            columns='Library', aggfunc='sum').fillna(0)

# Get the average number of visitors per open day in each library
visits_per_day = by_library_and_year/days_open

# Show the average number of visitors per open day for St. Boniface and Millennium libraries
plt.figure()
visits_per_day[['Millennium', 'St. Boniface']].plot(kind='bar')
plt.xticks(rotation = 45)
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Average number of visitors per day')
plt.gca().set_title('Average Number of Visitors per Day')
plt.gca().legend(loc='best', title='Library')

plt.show()