"""
Author: Ilyas El Boujadaini

Content: Interpolation of the time step for irregular real data.
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

"""Import the '11_real_data_interpolation_irregular_step' module using importlib and specify the module's name as string because
the file name starts with a number"""
import importlib
rdi = importlib.import_module("11_real_data_interpolation_irregular_step")

# Initializes the path to the csv file, adapting it to the user's OS
file_name = 'Enedis_SGE_HDM_A06GKIR0'
entry_path = os.path.join('input', file_name + '.csv')

# Empty dataframe to store the data
data = pd.DataFrame(columns=['date', 'power'])

# Read the csv file and store the data in the dataframe
with open(entry_path, "r", newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    for _ in range(3):
        next(csv_reader)
    
    # Store the data in the dataframe with the date as a datetime object and the power as an integer
    for line in csv_reader:
        date = dt.datetime.strptime(line[0].split('+')[0], "%Y-%m-%dT%H:%M:%S")
        if line[1] != '':
            data.loc[len(data)] = [date, int(line[1])]
        else:
            data.loc[len(data)] = [date, 0]

def verif_dup(data: pd.DataFrame, ind_step:int, wanted_step:int):
    """Verify if there is a similar date in the data and if the measures can be duplicated. Similar dates are dates that are 7 days
    apart with a limit of 3 weeks

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to check, columns are 'date' and 'power'.
        ind_step (int): the index of the irregular step to check.
        wanted_step (int): the wanted time step between each data point(in minutes).
    
    Returns:
        flag (bool): True if there is a substitute date, False otherwise.
        date (datetime): the substitute date if there is one, the same date with ind_step as index otherwise.
    """

    # We take the date of the irregular step and we look for a similar date in the data
    date = data['date'][ind_step]
    i = 1
    flag = False

    while i <= 3 and not flag:

        # Checks if the date is in the data within the 3 weeks limit
        date_1 = date + dt.timedelta(days=7*i)
        date_2 = date - dt.timedelta(days=7*i)
        include_1 = data['date'].isin([date_1]).any()
        include_2 = data['date'].isin([date_2]).any()

        # If the date is found, we store it in the variable date and put an end to the loop
        if include_1 :
            date = date_1
            flag = True
        elif include_2:
            date = date_2
            flag = True
        else:
            print('No date found')
        i+=1
    
    # Adds a column with the time step between each data point
    time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    data['time_step'] = [0] + time_step

    # We find the index of the date in the DataFrame
    index = data[data['date'] == date].index[0]
    print('index',index)
    step = data['time_step'][index]
    cumul_step = 0
    
    # We check the time step between the irregular step and the if the data is duplicable
    while index > 0 and cumul_step < step and flag:
        if data['time_step'][index] == data['time_step'][index-1]:
            cumul_step += data['time_step'][index]
            index -= 1
        else:
            flag = False
    
    del data['time_step']
    return flag, date

def data_duplication(data: pd.DataFrame, ind_step:int, wanted_step:int):
    """Duplicate the data if the time step is too big.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to duplicate, columns are 'date' and 'power'.
        ind_step (int): the index of the irregular step to check.
    
    Returns:
        res (pd.DataFrame): the duplicated data.
    """

    res = pd.DataFrame(columns=['date', 'power'])

    # We find the substitute date
    flag, date = verif_dup(data, ind_step, wanted_step)

    # Adds a column with the time step between each data point
    time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    data['time_step'] = [0] + time_step

    step = data['time_step'][ind_step]
    cumul_step = 0
    weeks = abs((date - data['date'][ind_step]).total_seconds() / 60 / 60 / 24 / 7)

    if flag:
        # We find the index of the date in the DataFrame
        index=data[data['date'] == date].index[0]
        step=data['time_step'][index]
        cumul_step = 0

        # We duplicate the data depending if the date we found is before or after the irregular step
        while index > 0 and cumul_step < step:
            if date > data['date'][ind_step]:
                res.loc[len(res)] = [data['date'][index] - dt.timedelta(days = 7*weeks), data['power'][index]]
            else:
                res.loc[len(res)] = [data['date'][index] + dt.timedelta(days = 7*weeks), data['power'][index]]
            index -= 1
        res.loc[len(res)] = [data['date'][ind_step], data['power'][ind_step]]

    return res
        
    
def dataset_correction(data: pd.DataFrame, wanted_step: int):
    """Correct the time step for irregular real data. Time step that are
    superior to 4 hours (240 minutes) are not corrected yet.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to correct, columns are 'date' and 'power'.
        wanted_step (int): the wanted time step between each data point(in minutes).
    
    Returns:
        res (pd.DataFrame): the corrected data.
    """
    
    res = pd.DataFrame(columns = ['date', 'power'])

    # Adds a column with the time step between each data point
    time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    data['time_step'] = [0] + time_step

    # At first, we use linear interpolation for low time steps
    res.loc[0] = [data['date'][0], data['power'][0]]
    for i in range(1,len(data)):
        if data['time_step'][i] > wanted_step and data['time_step'][i] < 240:
            res = pd.concat([res, rdi.lin_interpolation(data, i, wanted_step)], ignore_index = True)
        else:
            res.loc[len(res)] = [data['date'][i], data['power'][i]]

    time_step = (res['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    res['time_step'] = [0] + time_step
    # Then we duplicate the data for time steps superior to 240 minutes
    res2 = pd.DataFrame(columns = ['date', 'power'])
    for i in range(1,len(res)):
        if res['time_step'][i] >= 240:
            res2 = pd.concat([res2,data_duplication(res, i, wanted_step)], ignore_index = True)
    res=pd.concat([res,res2], ignore_index = True)
    res = res.sort_values(by='date').reset_index(drop=True)
    del res['time_step']
    del data['time_step']

    return res


data_corrected = dataset_correction(data, 60)
print(verif_dup(data_corrected, 364, 30))

# Verifies if the time step is corrected
time_step = (data_corrected['date'].diff() / pd.Timedelta(minutes = 1)).fillna(0)
data_corrected['time_step'] = [0] + time_step
step_change = data_corrected[data_corrected['time_step'] != data_corrected['time_step'].shift()]
print(step_change)

# Saves the corrected data in a csv file
exit_path = os.path.join('output',file_name + '_cleaned.csv')
data_corrected.to_csv(exit_path, sep = ';', index = False)