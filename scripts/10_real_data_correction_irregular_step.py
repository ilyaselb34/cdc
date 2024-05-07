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
        # Convertir la date en format datetime
        date = dt.datetime.strptime(line[0], "%Y-%m-%dT%H:%M:%S%z")
        if line[1] != '':
            # Ajouter la nouvelle ligne au DataFrame
            data.loc[len(data)] = [date, int(line[1])]
        else:
            # Si la puissance est vide, ajouter 0
            data.loc[len(data)] = [date, 0]
print(type(data))

time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data['time_step'] = [0]+time_step

step_change=data[data['time_step'] != data['time_step'].shift()]
print(step_change['time_step'])

def interpolation(data: pd.DataFrame, ind_step:int, wanted_step: int):
    """Data interpolation for irregular time step.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to interpolate.
        wanted_step (int): the wanted time step between each data point.
    
    Returns:
        res (pd.DataFrame): the interpolated data.
    """
    res = pd.DataFrame(columns=['date', 'power'])
    time_difference = (data['date'][ind_step] - data['date'][ind_step-1]).total_seconds() / 60
    x=time_difference//wanted_step-1
    pow_scale=(data['power'][ind_step] - data['power'][ind_step-1])/(int(x)-1)
    for i in range(int(x-1)):
        res.loc[len(res)] = [data['date'][ind_step-1] + dt.timedelta(minutes=wanted_step*(i)), data['power'][ind_step-1]+pow_scale*(i)]
    return res

df=interpolation(data, 161, 60)
print(df)