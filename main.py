import os
import sys
import pandas as pd
import argparse

# Ajoutez les répertoires nécessaires au chemin système
current_dir = os.path.dirname(os.path.abspath(__file__))
tools_dir = os.path.join(current_dir, 'tools')
sys.path.append(tools_dir)

# Importez vos modules
import correction as crct  # type: ignore
import delimiter as dlmt  # type: ignore


def main(file_name: str, timestep: int):
    entry_path = os.path.join('input', file_name)
    delimiter = dlmt.detect_delimiter(entry_path)
    data = pd.read_csv(entry_path, sep=delimiter, header=2)
    data['date'] = pd.to_datetime(data['Horodate'].str.split('+').str[0],
                                  format="%Y-%m-%dT%H:%M:%S")
    del data['Horodate']
    data['puissance_w'] = data['Valeur']
    del data['Valeur']
    data['valeur_mesuree'] = 'Oui'

    # We call the main function, verify the time step between each
    # data point and export the final result in a csv file

    data_corrected = crct.dataset_correction(data, timestep)
    data_corrected['pas_temps'] = [0] + (data_corrected['date'].diff()
                                         / pd.Timedelta(minutes=1)).fillna(0)
    step_change = data_corrected[data_corrected['pas_temps']
                                 != data_corrected['pas_temps'].shift()]
    print(step_change)
    exit_path = os.path.join('output', file_name[:-4] + '_cleaned' + '.csv')
    data_corrected.to_csv(exit_path, sep=',', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process and clean '
                                     'a CSV file.')
    parser.add_argument('--input_csv', "-i", type=str, help='nom ficher csv')
    parser.add_argument('--timestep', '-t', type=int, help='pas temporel en '
                        'minutes')

    args = parser.parse_args()

    main(args.file_name, args.timestep)
