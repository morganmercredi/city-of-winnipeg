"""
Simple data exploration using the City of Winnipeg's "Library People Counts" dataset.

The dataset can be downloaded here: 
https://data.winnipeg.ca/Libraries/Library-People-Counts/g3zt-s3kr/data
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Path to file (for me)
file_path = '../../Sample Data Sets/Library_People_Counts.csv'

# Read the file
counts = pd.read_csv(file_path)

# Remove the count IDs
counts = counts.drop(labels='ID', axis=1)

# Set the week as the index
counts = counts.set_index('Week End Date')

# Make the weeks into a time
counts.index = pd.to_datetime(counts.index)

# Go through the description column and separate out the library name only
counts['Library'] = [" ".join(desc.split()[:-4]) for desc in counts['Description']]

# Get the number of total counts per year in each library
by_library_and_year = counts.groupby(['Library', counts.index.year])['Count'].sum()
by_library_and_year = by_library_and_year.unstack(level=0).fillna(0)

# Alternatively...
by_library_and_year = counts.pivot_table('Count', index=counts.index.year,
                                         columns='Library', aggfunc='sum').fillna(0)

# Show the number of visitors per year for select libraries
plt.figure()
ax1 = by_library_and_year[['St. Boniface', 'St. Vital']].plot(kind='bar')
ax1.set_xlabel('Year')
ax1.set_ylabel('Visits')
ax1.set_title('Yearly Visits')

# Group counts by year
by_year = counts.groupby(counts.index.year)['Count'].sum()

# Show the total visitors per year
plt.figure()
ax2 = by_year.plot(kind='bar')
ax2.set_xlabel('Year')
ax2.set_ylabel('Visits')
ax2.set_title('Yearly Visits')

# Get the number of visitors per month in each library
by_library_and_month = counts.pivot_table('Count', index=counts.index.month,
                                          columns='Library', aggfunc='sum').fillna(0)

# Show the number of visitors each month for select libraries
plt.figure()
ax3 = by_library_and_month[['St. Boniface', 'Cornish']].plot(kind='bar')
ax3.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                           'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax3.set_xlabel('Month')
ax3.set_ylabel('Visits')
ax3.set_title('Monthly Visits')