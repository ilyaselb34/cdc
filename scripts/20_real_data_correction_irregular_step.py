"""
Author: Ilyas El Boujadaini

Content: Interpolation of the time step for irregular real data.
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

# Import the "11_real_data_interpolation_irregular_step" module using importlib et specify the module's name as string because the file name starts with a number
import importlib
rdi = importlib.import_module("11_real_data_interpolation_irregular_step")

data = pd.DataFrame(columns=['date', 'power'])

file_name = 'Enedis_SGE_HDM_A06GKIR0'
entry_path = os.path.join('input', file_name + '.csv')

with open(entry_path, "r", newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    for _ in range(3):
        next(csv_reader)
    for line in csv_reader:
        # to convert the date to datetime format
        date = dt.datetime.strptime(line[0], "%Y-%m-%dT%H:%M:%S%z")
        if line[1] != '':
            # Add the new line to the DataFrame
            data.loc[len(data)] = [date, int(line[1])]
        else:
            # if the power is empty, add 0
            data.loc[len(data)] = [date, 0]

def duplication(data: pd.DataFrame, ind_step: int, wanted_step: int):
    """Duplicate multiple rows from the dataframe to fill a time step in case it is too large.

    Args:
        data (pd.DataFrame): pandas DataFrame with the data to correct, columns are 'date' and 'power'.
        ind_step (int): the index of the data point where the time step is too much important.
    
    Returns:
        res (pd.DataFrame): the corrected data, returning the power data from the same time interval one day earlier.
    """

    res=pd.DataFrame(columns=['date', 'power'])
    date = data['date'][ind_step] - dt.timedelta(days=1)

    i = data[data['date'] == date].index[0]
    while data['date'][i].date() == date.date():
        i -= 1
        new_date = date - dt.timedelta(minute=wanted_step)
        res.loc[len(res)] = [new_date, data['power'][ind_step]]

    return res

def dataset_correction(data: pd.DataFrame, wanted_step: int):
    """Correct the time step for irregular real data.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to correct, columns are 'date' and 'power'.
        wanted_step (int): the wanted time step between each data point(in minutes).
    
    Returns:
        res (pd.DataFrame): the corrected data.
    """

    res=pd.DataFrame(columns=['date', 'power'])

    #Creating a copy of the dataframe not to modify the original one and to find the irregular time steps
    time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    data['time_step'] = [0]+time_step
    step_change=data[data['time_step'] != data['time_step'].shift()]


    res.loc[0] = [data['date'][0], data['power'][0]]
    for i in range(1,len(data)):
        if data['time_step'][i]>wanted_step:
            res = pd.concat([res, rdi.interpolation(data, i, wanted_step)], ignore_index=True)
        else:
            res.loc[len(res)] = [data['date'][i], data['power'][i]]

    del data['time_step']

    return res
#Creating a copy of the dataframe not to modify the original one and to find the irregular time steps
time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data['time_step'] = [0]+time_step
step_change=data[data['time_step'] != data['time_step'].shift()]
print(step_change)

data_corrected = dataset_correction(data, 60)
exit_path = os.path.join('output',file_name + '_cleaned.csv')
data_corrected.to_csv(exit_path, sep=',', index=False, header=True, encoding='utf-8')