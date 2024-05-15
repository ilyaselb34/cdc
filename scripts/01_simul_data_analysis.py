"""
Author: Ilyas El Boujadaini

Content: Analysis of simulated data (calculation of average power per day)
"""

# Imports necessary libraries for paths
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
path_repo = str(os.path.dirname(current_dir))

# Necessary libraries for data analysis
import csv
import pandas as pd
import datetime as dt

# Initializes the path to the csv file, adapting it to the user's OS
entry_path = os.path.join('output', '00_simulation_20min_const.csv')
simul = []

"""Reads the csv file and converts the date to datetime format and the power to
integer"""
with open(entry_path, "r", newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    for line in csv_reader:
        line[0] = dt.datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')
        line[1] = int(line[1])
        simul.append(line)


def average_daily_power(simul):
    """Calculates the average power per day from a list of simulated data

    Args:
        simul (list): data list with date and power values

    Returns:
        daily_average (pd.Dataframe): dataframe with the average power per day
    """

    """Formats the data into a pandas dataframe and calculates the average
    power per day"""
    df = pd.DataFrame(simul, columns=['date', 'power'])
    daily_average = (
        df.groupby(df['date'].dt.date)
        ['power']
        .mean()
        .reset_index()
    )

    return daily_average


# Calls the function and prints the first 5 rows of the result
res = average_daily_power(simul)
print(res.head(5))

# Exports the result to a csv file
exit_path = os.path.join('output', '01_simulation_analysis.csv')
res.to_csv(exit_path, sep=';', index=False, header=False, encoding='utf-8')
