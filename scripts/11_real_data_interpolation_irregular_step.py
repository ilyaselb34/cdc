"""
Author: Ilyas El Boujadaini

Content: Linear interpolation of the time step for irregular real data.
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
file_name = 'Enedis_SGE_HDM_A06GKIR0'
entry_path = os.path.join('input', file_name + '.csv')

# Empty dataframe to store the data
data = pd.DataFrame(columns=['date', 'power'])

# Reads the data from the csv file
with open(entry_path, "r", newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")

    """Skips the first 3 lines of the file because their data are irrelevant to
    the analysis"""
    for _ in range(3):
        next(csv_reader)

    """Reads the data and converts the date to datetime format and the power to
    integer"""
    for line in csv_reader:
        date = dt.datetime.strptime(line[0], "%Y-%m-%dT%H:%M:%S%z")
        if line[1] != '':
            data.loc[len(data)] = [date, int(line[1])]
        else:
            data.loc[len(data)] = [date, 0]


def lin_interpolation(data: pd.DataFrame, ind_step: int, wanted_step: int):
    """Data linear interpolation for irregular time step. Also interpolates
    whole days if the time step is too big, so we have to improve this
    functionnality later.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to interpolate,
            columns are 'date' and 'power'.
        ind_step (int): the index of the irregular step to correct.
        wanted_step (int): the wanted time step between each data point
            (in minutes).

    Returns:
        res (pd.DataFrame): the interpolated data.
    """

    # Creating a new dataframe to store the interpolated data
    res = pd.DataFrame(columns=['date', 'power'])

    """Adds data points to the new dataframe, adapting the power value to the
    time step"""
    time_step = (data['date'][ind_step]
                 - data['date'][ind_step-1]).total_seconds() / 60
    x = time_step//wanted_step
    pow_scale = (data['power'][ind_step] - data['power'][ind_step-1])/(int(x))
    for i in range(1, int(x)):
        res.loc[len(res)] = [data['date'][ind_step-1]
                             + dt.timedelta(minutes=(wanted_step*i)),
                             data['power'][ind_step-1]+pow_scale*(i)]
    res.loc[len(res)] = [data['date'][ind_step], data['power'][ind_step]]

    return res


df = lin_interpolation(data, 1439, 30)


def dataset_lin_interpolation(data: pd.DataFrame, wanted_step: int):
    """Interpolate the time step for irregular real data.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to interpolate,
            columns are 'date' and 'power'.
        wanted_step (int): the wanted time step between each data point
            (in minutes).

    Returns:
        res (pd.DataFrame): the corrected data.
    """

    res = pd.DataFrame(columns=['date', 'power'])

    """Adds a new column to the dataframe with the time step between each data
    point"""
    time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    data['time_step'] = [0]+time_step

    """Interpolates the data points with a time step bigger than the wanted
    time step"""
    res.loc[0] = [data['date'][0], data['power'][0]]
    for i in range(1, len(data)):
        if data['time_step'][i] > wanted_step:
            res = pd.concat([res, lin_interpolation(data, i, wanted_step)],
                            ignore_index=True)
        else:
            res.loc[len(res)] = [data['date'][i], data['power'][i]]

    del data['time_step']

    return res


# Calls the function
data_interpolated = dataset_lin_interpolation(data, 60)

# Verifies that the time step between each data point has been corrected
time_step = (data_interpolated['date'].diff()
             / pd.Timedelta(minutes=1)).fillna(0)
data_interpolated['time_step'] = [0]+time_step

# Saves the corrected data to a new csv file
exit_path = os.path.join('output', file_name + '_cleaned.csv')
data_interpolated.to_csv(exit_path, sep=',', index=False, header=True,
                         encoding='utf-8')
