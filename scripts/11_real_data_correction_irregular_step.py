"""
Author: Ilyas El Boujadaini

Content: Correction of the time step for irregular real data.
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

def interpolation(data: pd.DataFrame, ind_step:int, wanted_step: int):
    """Data interpolation for irregular time step. Also interpolates whole days if the time step is too big, so we have to improve this functionnality later.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to interpolate, columns are 'date' and 'power'.
        ind_step (int): the index of the irregular step to correct.
        wanted_step (int): the wanted time step between each data point(in minutes).
    
    Returns:
        res (pd.DataFrame): the interpolated data.
    """
    res = pd.DataFrame(columns=['date', 'power'])
    time_step=(data['date'][ind_step] - data['date'][ind_step-1]).total_seconds() / 60
    x=time_step//wanted_step
    print('coucou',x)
    pow_scale=(data['power'][ind_step] - data['power'][ind_step-1])/(int(x))
    for i in range(1,int(x)):
        res.loc[len(res)] = [data['date'][ind_step-1] + dt.timedelta(minutes=(wanted_step*i)), data['power'][ind_step-1]+pow_scale*(i)]
    res.loc[len(res)] = [data['date'][ind_step], data['power'][ind_step]]
    return res

df=interpolation(data, 1439, 30)
print(df)

def data_correction(data: pd.DataFrame, wanted_step: int):
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
            res = pd.concat([res, interpolation(data, i, wanted_step)], ignore_index=True)
        else:
            res.loc[len(res)] = [data['date'][i], data['power'][i]]

    del data['time_step']

    return res

data_corrected=data_correction(data, 60)
time_step = (data_corrected['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data_corrected['time_step'] = [0]+time_step
step_change=data_corrected[data_corrected['time_step'] != data_corrected['time_step'].shift()]
print(step_change)
exit_path = os.path.join('output',file_name + '_cleaned.csv')
data_corrected.to_csv(exit_path, sep=',', index=False, header=True, encoding='utf-8')