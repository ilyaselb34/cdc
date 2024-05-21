"""
Author: Ilyas El Boujadaini

Content: Interpolation of the time step for irregular real data.
"""

import os
import sys
import datetime as dt
import csv
import pandas as pd

# Obtenez le chemin absolu du répertoire parent du script actuel
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construisez le chemin du dossier tools
tools_dir = os.path.join(parent_dir, 'tools')

# Ajoutez le dossier tools au chemin de recherche
sys.path.append(tools_dir)

# Importez le module correction
import correction as crct



# Initializes the path to the csv file, adapting it to the user's OS
file_name = 'Enedis_SGE_HDM_A06GKIR0'
entry_path = os.path.join('input', file_name + '.csv')

# Empty dataframe to store the data
data = pd.DataFrame(columns=['date', 'puissance_w', 'valeur_mesuree'])

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
            data.loc[len(data)] = [date, int(line[1]), 'Oui']
        else:
            data.loc[len(data)] = [date, 0, 'Oui']


# We call the main function, verify the time step between each data point and
# export the final result in a csv file
data_corrected = crct.dataset_correction(data, 60)
time_step = (data_corrected['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data_corrected['time_step'] = [0] + time_step
step_change = data_corrected[data_corrected['time_step']
                             != data_corrected['time_step'].shift()]
print(step_change)
exit_path = os.path.join('output', file_name + '_cleaned.csv')
data_corrected.to_csv(exit_path, sep=',', index=False)
