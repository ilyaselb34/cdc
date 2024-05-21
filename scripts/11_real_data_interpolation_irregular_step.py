"""
Author: Ilyas El Boujadaini

Content: Linear interpolation of the time step for irregular real data.
"""

# Imports necessary libraries for paths
import os

# Necessary libraries for data analysis
import datetime as dt
import csv
import pandas as pd

import tools.linear_interpolation as itrp

# Initializes the path to the csv file, adapting it to the user's OS
file_name = 'Enedis_SGE_HDM_A06GKIR0'
entry_path = os.path.join('input', file_name + '.csv')

# Empty dataframe to store the data
data = pd.DataFrame(columns=['date', 'power', 'empirical'])

# Reads the data from the csv file
with open(entry_path, "r", newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")

    # Skips the first 3 lines of the file because their data are irrelevant to
    # the analysis
    for _ in range(3):
        next(csv_reader)

    # Reads the data and converts the date to datetime format and the power to
    # integer
    for line in csv_reader:
        date = dt.datetime.strptime(line[0], "%Y-%m-%dT%H:%M:%S%z")
        if line[1] != '':
            data.loc[len(data)] = [date, int(line[1]), 1]
        else:
            data.loc[len(data)] = [date, 0, 1]


df = itrp.linear_interpolation(data, 1439, 30)

# Calls the function
data_interpolated = itrp.dataset_linear_interpolation(data, 60)

# Verifies that the time step between each data point has been corrected
time_step = (data_interpolated['date'].diff()
             / pd.Timedelta(minutes=1)).fillna(0)
data_interpolated['time_step'] = [0]+time_step
step_change = data_interpolated[data_interpolated['time_step']
                                != data_interpolated['time_step'].shift()]
print(step_change)

# Saves the corrected data to a new csv file
exit_path = os.path.join('output', file_name + '_cleaned.csv')
data_interpolated.to_csv(exit_path, sep=',', index=False, header=True,
                         encoding='utf-8')
