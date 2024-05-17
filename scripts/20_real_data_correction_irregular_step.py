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

# Import the '11_real_data_interpolation_irregular_step' module using
# importlib and specify the module's name as string because
# the file name starts with a number
import importlib
rdi = importlib.import_module("11_real_data_interpolation_irregular_step")

# Initializes the path to the csv file, adapting it to the user's OS
file_name = 'Enedis_SGE_HDM_A06GKIR0'
entry_path = os.path.join('input', file_name + '.csv')

# Empty dataframe to store the data
data = pd.DataFrame(columns=['date', 'power', 'empirical'])

# Read the csv file and store the data in the dataframe
with open(entry_path, "r", newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    for _ in range(3):
        next(csv_reader)

    # Store the data in the dataframe with the date as a datetime object and
    # the power as an integer
    for line in csv_reader:
        date = dt.datetime.strptime(line[0].split('+')[0], "%Y-%m-%dT%H:%M:%S")
        if line[1] != '':
            data.loc[len(data)] = [date, int(line[1]), 1]
        else:
            data.loc[len(data)] = [date, 0, 1]

data = data.sort_values(by='date').reset_index(drop=True)
print(data.head(10))


def duplicable(data: pd.DataFrame, time: dt.datetime, wanted_step: int):
    res = True
    time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    data['time_step'] = [0] + time_step
    i = data[data['date'] == date].index[0]
    cumul_step = 0
    if data['date'].isin([time]).any():
        while (i >= 0 and cumul_step < wanted_step and res):
            if data['time_step'][i] > wanted_step:
                res = False
            else:
                cumul_step += data['time_step'][i]
                i -= 1
            if i == 0:
                res = False
    else:
        res = False
    return res


def data_duplication(data: pd.DataFrame, ind_step: int, wanted_step: int):
    """Duplicate the data if the time step is too big.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to duplicate,
            columns are 'date' and 'power'.
        ind_step (int): the index of the irregular step to check.

    Returns:
        res (pd.DataFrame): the duplicated data.
    """

    res = pd.DataFrame(columns=['date', 'power', 'empirical'])

    # We check if a substitution date is available
    date_found = False
    i = 1
    while (i <= 3 and not date_found):
        if data['date'].isin([data['date'][ind_step]
                             + dt.timedelta(days=i * 7)]).any():
            sub_date = data['date'][ind_step] + dt.timedelta(days=i * 7)
            if duplicable(data, sub_date, wanted_step):
                date_found = True
                weeks = -i
                print('sub_date', sub_date)
            print('sub_date', sub_date)
        elif data['date'].isin([data['date'][ind_step]
                               - dt.timedelta(days=i * 7)]).any():
            sub_date = data['date'][ind_step] - dt.timedelta(days=i * 7)
            if duplicable(data, sub_date, wanted_step):
                date_found = True
                weeks = i
            print('sub_date', sub_date)
        i += 1
    print('boucle', weeks)

    # If a substitution date is found, we check if the data is duplicable
    if date_found:
        time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
        data['time_step'] = [0] + time_step
        j = data[data['date'] == sub_date].index[0]
        cumul_step = 0
        while (j > 0 and
               cumul_step < data['time_step'][ind_step] and
               date_found):
            if data['time_step'][j] > wanted_step:
                date_found = False
            else:
                res.loc[len(res)] = [data['date'][j], data['power'][j], 0]
                cumul_step += data['time_step'][j]
                j -= 1
        res['date'] = res['date'] + dt.timedelta(days=7 * weeks)
    else:
        print('No substitution date found.')
        res = pd.DataFrame(columns=['date', 'power', 'empirical'])
    res.loc[len(res)] = [data['date'][ind_step], data['power'][ind_step], 1]
    return res


def dataset_correction(data: pd.DataFrame, wanted_step: int):
    """Correct the time step for irregular real data. Time step that are
    superior to 4 hours (240 minutes) are not corrected yet.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to correct,
            columns are 'date' and 'power'.
        wanted_step (int): the wanted time step between each data point
            (in minutes).

    Returns:
        res (pd.DataFrame): the corrected data.
    """

    res = pd.DataFrame(columns=['date', 'power', 'empirical'])

    # Adds a column with the time step between each data point
    time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    data['time_step'] = [0] + time_step

    # At first, we use linear interpolation for low time steps
    res.loc[0] = [data['date'][0], data['power'][0], data['empirical'][0]]
    for i in range(1, len(data)):
        if data['time_step'][i] > wanted_step and data['time_step'][i] < 240:
            res = pd.concat([res, rdi.lin_interpolation(data, i, wanted_step)],
                            ignore_index=True)
        else:
            res.loc[len(res)] = [data['date'][i], data['power'][i],
                                 data['empirical'][i]]

    time_step = (res['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    res['time_step'] = [0] + time_step

    # Then we duplicate the data for time steps superior to 240 minutes
    res2 = pd.DataFrame(columns=['date', 'power', 'empirical'])
    for i in range(1, len(data)):
        if data['time_step'][i] >= 240:
            res2 = pd.concat([res2, data_duplication(data, i, wanted_step)],
                             ignore_index=True)
    res = pd.concat([res, res2], ignore_index=True)
    res = res.sort_values(by='date').reset_index(drop=True)
    del res['time_step']
    del data['time_step']

    return res


data_corrected = dataset_correction(data, 60)

# Verifies if the time step is corrected
time_step = (data_corrected['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data_corrected['time_step'] = [0] + time_step
step_change = data_corrected[data_corrected['time_step']
                             != data_corrected['time_step'].shift()]
print(step_change)
# Saves the corrected data in a csv file
exit_path = os.path.join('output', file_name + '_cleaned.csv')
data_corrected.to_csv(exit_path, sep=',', index=False)
dup = data_duplication(data, 362, 60)
dup.to_csv('dup.csv', sep=',', index=False)
