"""
Author: Ilyas El Boujadaini

Content: Completion of the time step for complete real data by linear
interpolation, for the first try we will use the Enedis_SGE_HDM_A0622AU5.csv
file and we will correct the time step to be 30 minutes between each data
point.
"""

# Imports necessary libraries for paths
import os
import sys

# Adds the path to the project root to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
path_repo = str(os.path.dirname(current_dir))

# Necessary libraries for data analysis
import datetime as dt
import csv
import pandas as pd

# Initializes the path to the csv file, adapting it to the user's OS
file_name = 'Enedis_SGE_HDM_A0622AU5'
entry_path = os.path.join('input', file_name + '.csv')

# Empty dataframe to store the data
data = pd.DataFrame(columns=['date', 'power', 'empirical'])

# Reads the data from the csv file
with open(entry_path, "r", newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")

    """Skips the first 3 lines of the file because their data are irrelevant
    to the analysis"""
    for _ in range(3):
        next(csv_reader)

    """Reads the data and converts the date to datetime format and the power to
    integer"""
    for line in csv_reader:
        date = dt.datetime.strptime(line[0], "%Y-%m-%dT%H:%M:%S%z")
        if line[1] != '':
            data.loc[len(data)] = [date, int(line[1]), 1]
        else:
            data.loc[len(data)] = [date, 0, 1]

"""Adds a time step column to the dataframe, showing the time difference
between each data point"""
time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data['time_step'] = [0]+time_step
print(data[data['time_step'] != data['time_step'].shift()])
del data['time_step']

# Creates a new dataframe to store the interpolated data
data2 = pd.DataFrame(columns=['date', 'power', 'empirical'])

# Iterates through the rows of the DataFrame
for i in range(len(data) - 1):
    time_difference = (data['date'][i + 1]
                       - data['date'][i]).total_seconds() / 60
    if time_difference == 60:
        new_date = data['date'][i] + dt.timedelta(minutes=30)
        average_power = (data['power'][i] + data['power'][i + 1]) / 2
        data2.loc[len(data2)] = [new_date, average_power, 1]

# Concatenates the two DataFrames and sorts the values by date
data = pd.concat([data, data2], ignore_index=True)
data = data.sort_values(by='date').reset_index(drop=True)

# Adds the time step column again to verify the interpolation
time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data['time_step'] = [0]+time_step
print(data['time_step'].value_counts())

# Exports the data to a new csv file
exit_path = os.path.join('output', file_name + '_cleaned.csv')
data.to_csv(exit_path, sep=',', index=False, header=True, encoding='utf-8')
