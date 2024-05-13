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

# Import the "11_real_data_interpolation_irregular_step" module using importlib and specify the module's name as string because the file name starts with a number
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

def verif_dup(data: pd.DataFrame, ind_step:int, wanted_step:int):
    """Verify if there is a similar date in the data with a wanted time step between them. Similar dates are dates that are 7 days
    apart with a limit of 3 weeks

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to check, columns are 'date' and 'power'.
        ind_step (int): the index of the irregular step to check.
        wanted_step (int): the wanted time step between each data point(in minutes).
    
    Returns:
        res (bool): True if the time step is too big, False otherwise.
    """
    date=data['date'][ind_step]
    i=1
    date_found=False
    print('wesh',date )
    while i<=3 and not date_found:
        date_1 = date + dt.timedelta(days=7*i)
        date_2 = date - dt.timedelta(days=7*i)
        if date_1 in data['date'] :
            date=date_1
            date_found=True
        elif date_2 in data['date']:
            date=date_2
            date_found=True
        else:
            print('No date found')
        i+=1
    return date_found
        
    
def dataset_correction(data: pd.DataFrame, wanted_step: int):
    """Correct the time step for irregular real data. Time step that are superior to 4 hours (240 minutes) are not corrected yet.

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
        if data['time_step'][i]>wanted_step and data['time_step'][i]<240:
            res = pd.concat([res, rdi.interpolation(data, i, wanted_step)], ignore_index=True)
        else:
            res.loc[len(res)] = [data['date'][i], data['power'][i]]

    del data['time_step']

    return res

data_corrected=dataset_correction(data, 60)
print(verif_dup(data_corrected, 364, 30))
#Creating a copy of the dataframe not to modify the original one and to find the irregular time steps
time_step = (data_corrected['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data_corrected['time_step'] = [0]+time_step
step_change=data_corrected[data_corrected['time_step'] != data_corrected['time_step'].shift()]
print(step_change)


exit_path = os.path.join('output',file_name + '_cleaned.csv')
data_corrected.to_csv(exit_path, sep=';', index=False)

print(data_corrected['date'][1443])