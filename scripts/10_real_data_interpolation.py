"""
Author: Ilyas El Boujadaini

Content: Correction of the time step for complete real data, for the first try we will use the Enedis_SGE_HDM_A0622AU5.csv file and we will correct the time step to be 30 minutes between each data point.
"""

#import necessary libraries
import os   #for paths
import sys  #for paths

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
path_repo = str(os.path.dirname(current_dir))

import datetime as dt #for dates
from random import * #for random power values
import csv #for exporting
import pandas as pd #for dataframes

data = pd.DataFrame(columns=['date', 'power'])

file_name = 'Enedis_SGE_HDM_A0622AU5'
entry_path = os.path.join('input', file_name + '.csv')

with open(entry_path, "r", newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for _ in range(3):
        next(csv_reader)
    for line in csv_reader:
        # Convertir la date en format datetime
        date = dt.datetime.strptime(line[0], "%Y-%m-%dT%H:%M:%S%z")
        if line[1] != '':
            # Ajouter la nouvelle ligne au DataFrame
            data.loc[len(data)] = [date, int(line[1])]
        else:
            # Si la puissance est vide, ajouter 0
            data.loc[len(data)] = [date, 0]

#creating a dataframe for easier calculations and adding the time step between each data point to the dataframe
time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data['time_step'] = [0]+time_step
print(data[data['time_step'] != data['time_step'].shift()])#we can see that the time step is not constant and where it changes

new_lines = []
# Iterate through the rows of the DataFrame
for i in range(len(data) - 1):
    # Check if the time difference between dates is 60 minutes
    time_difference = (data['date'][i + 1] - data['date'][i]).total_seconds() / 60
    if time_difference == 60:
        # Calculate the average power
        average_power = (data['power'][i] + data['power'][i + 1]) / 2
        # Calculate the new date
        new_date = data['date'][i] + dt.timedelta(minutes=30)
        # Create a new row with the average power and the new date
        new_row = {'date': new_date, 'power': average_power}
        # Add the new row to the list
        new_lines.append(new_row)
data2 = pd.DataFrame(new_lines)

data = pd.concat([data, data2], ignore_index=True)
data=data.sort_values(by='date').reset_index(drop=True) #sorting the dataframe by date
print(data.head(20))

del data['time_step'] #removing the time step column
print(data.head(20))

time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data['time_step'] = [0]+time_step
print(data.head(20))
print(data['time_step'].value_counts())

exit_path = os.path.join('output',file_name + '_cleaned.csv')
data.to_csv(exit_path, sep=',', index=False, header=True, encoding='utf-8')