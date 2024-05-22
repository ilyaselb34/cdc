"""
Author: Ilyas El Boujadaini

Content: Completion of the time step for complete real data by linear
interpolation, for the first try we will use the Enedis_SGE_HDM_A0622AU5.csv
file and we will correct the time step to be 30 minutes between each data
point.
"""

import os
import sys
import datetime as dt
import pandas as pd

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tools_dir = os.path.join(parent_dir, 'tools')
sys.path.append(tools_dir)
import delimiter as dlmt  # type: ignore

# Initializes the path to the csv file, adapting it to the user's OS
file_name = 'Enedis_SGE_HDM_A0622AU5'
entry_path = os.path.join('input', file_name + '.csv')
delimiter = dlmt.detect_delimiter(entry_path)
data = pd.read_csv(entry_path, sep=delimiter, header=2)

data['date'] = pd.to_datetime(data['Horodate'].str.split('+').str[0],
                              format="%Y-%m-%dT%H:%M:%S")
del data['Horodate']
data['puissance_w'] = data['Valeur']
del data['Valeur']
data['valeur_mesuree'] = 'Oui'

"""Adds a time step column to the dataframe, showing the time difference
between each data point"""
time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data['time_step'] = [0] + time_step
print(data[data['time_step'] != data['time_step'].shift()])
del data['time_step']

# Creates a new dataframe to store the interpolated data
data2 = pd.DataFrame(columns=['date', 'power', 'empirical'])

# Iterates through the rows of the DataFrame
for i in range(len(data) - 1):
    time_difference = (data['date'][i + 1] - data['date'][i]
                       ).total_seconds() / 60
    if time_difference == 60:
        new_date = data['date'][i] + dt.timedelta(minutes=30)
        average_power = (data['power'][i] + data['power'][i + 1]) / 2
        data2.loc[len(data2)] = [new_date, average_power, 1]

# Concatenates the two DataFrames and sorts the values by date
data = pd.concat([data, data2], ignore_index=True)
data = data.sort_values(by='date').reset_index(drop=True)

# Adds the time step column again to verify the interpolation
time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data['time_step'] = [0] + time_step
print(data['time_step'].value_counts())

# Exports the data to a new csv file
exit_path = os.path.join('output', file_name + '_cleaned.csv')
data.to_csv(exit_path, sep=',', index=False, header=True, encoding='utf-8')
