"""
Author: Ilyas El Boujadaini

Content: Interpolation of the time step for irregular real data.
"""

import os
import sys
import pandas as pd

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tools_dir = os.path.join(parent_dir, 'tools')
sys.path.append(tools_dir)
import correction as crct  # type: ignore
import delimiter as dlmt  # type: ignore


# Initializes the path to the csv file, adapting it to the user's OS
file_name = 'Enedis_SGE_HDM_A06GKIR0'
entry_path = os.path.join('input', file_name + '.csv')

delimiter = dlmt.detect_delimiter(entry_path)
data = pd.read_csv(entry_path, sep=delimiter, header=2)
data['date'] = pd.to_datetime(data['Horodate'].str.split('+').str[0],
                              format="%Y-%m-%dT%H:%M:%S")
del data['Horodate']
data['puissance_w'] = data['Valeur']
del data['Valeur']
data['valeur_mesuree'] = 'Oui'

# We call the main function, verify the time step between each data point and
# export the final result in a csv file

data_corrected = crct.dataset_correction(data, 60)
pas_temps = (data_corrected['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
data_corrected['pas_temps'] = [0] + pas_temps
step_change = data_corrected[data_corrected['pas_temps'] != data_corrected[
    'pas_temps'].shift()]
print(step_change)
exit_path = os.path.join('output', file_name + '_cleaned.csv')
data_corrected.to_csv(exit_path, sep=',', index=False)
