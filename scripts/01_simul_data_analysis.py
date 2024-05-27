"""
Author: Ilyas El Boujadaini

Content: Analysis of simulated data (calculation of average power per day)
"""

# Imports necessary libraries for paths
import os
import pandas as pd

import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tools_dir = os.path.join(parent_dir, 'tools')
sys.path.append(tools_dir)
import delimiter as dlmt  # type: ignore

# Initializes the path to the csv file, adapting it to the user's OS
entry_path = os.path.join('input', '00_simulation_20min_const.csv')

# Reads the csv file and converts the date to datetime format and
# the power to integer
delimiter = dlmt.detect_delimiter(entry_path)
simul = pd.read_csv(entry_path, sep=delimiter)
simul['date'] = pd.to_datetime(simul['date'].str.split('+').str[0],
                               format="%Y-%m-%d %H:%M:%S")
print(simul.head(5))


def average_daily_power(simul):
    """Calculates the average power per day from a list of simulated data

    Args:
        simul (list): data list with date and power values

    Returns:
        daily_average (pd.Dataframe): dataframe with the average power per day
    """

    """Formats the data into a pandas dataframe and calculates the average
    power per day"""
    df = pd.DataFrame(simul, columns=['date', 'puissance_w'])
    daily_average = (
        df.groupby(df['date'].dt.date)
        ['puissance_w']
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
