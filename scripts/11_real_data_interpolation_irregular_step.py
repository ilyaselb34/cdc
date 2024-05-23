"""
Author: Ilyas El Boujadaini

Content: Linear interpolation of the time step for irregular real data.
"""

import os
import sys
import pandas as pd
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tools_dir = os.path.join(parent_dir, 'tools')
sys.path.append(tools_dir)
import linear_interpolation as itrp  # type: ignore
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

df = itrp.linear_interpolation(data, 1439, 30)

# Calls the function
data_interpolated = itrp.dataset_linear_interpolation(data, 60)

# Verifies that the time step between each data point has been corrected
data_interpolated['pas_temps'] = [0] + (data_interpolated['date'].diff()
                                        / pd.Timedelta(minutes=1)).fillna(0)
step_change = data_interpolated[data_interpolated[
    'pas_temps'] != data_interpolated['pas_temps'].shift()]
print(step_change)

# Saves the corrected data to a new csv file
exit_path = os.path.join('output', file_name + '_cleaned.csv')
data_interpolated.to_csv(exit_path, sep=',', index=False, header=True,
                         encoding='utf-8')
