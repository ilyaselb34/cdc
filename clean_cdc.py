#!/usr/bin/env python

import os
import sys
import pandas as pd
import argparse
import locale
import re

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

current_dir = os.path.dirname(os.path.abspath(__file__))
tools_dir = os.path.join(current_dir, 'tools')
sys.path.append(tools_dir)
import correction as crct  # type: ignore
import delimiter as dlmt  # type: ignore


def main(file_name: str, timestep: int):
    delimiter = dlmt.detect_delimiter(file_name)
    data = pd.read_csv(file_name, sep=delimiter, header=2)
    data['date'] = pd.to_datetime(data['Horodate'].str.split('+').str[0],
                                  format="%Y-%m-%dT%H:%M:%S")
    del data['Horodate']
    data['puissance_w'] = data['Valeur']
    del data['Valeur']

    # We call the main function, verify the time step between each
    # data point and export the final result in a csv file
    print('Le fichier', file_name, 'contient des données mesurées entre les',
          'dates suivantes :', data['date'][0], 'et', data['date'][len(data)
                                                                   - 1])

    data_corrected = crct.dataset_correction(data, timestep)
    data_corrected['jour_semaine'] = data_corrected['date'].dt.strftime('%A')
    data_corrected['pas_temps'] = [0] + (data_corrected['date'].diff()
                                         / pd.Timedelta(minutes=1)).fillna(0)
    step_change = data_corrected[data_corrected['pas_temps']
                                 != data_corrected['pas_temps'].shift()]
    print('Le tableau suivant montre si il y a une variation du pas temporel')
    print(step_change, '\n\n\n')

    pattern = r'(Enedis.*?\.csv)'
    match = re.search(pattern, file_name)
    result = match.group(1)
    exit_path = os.path.join('output', result[:-4] + '_cleaned.csv')

    data_corrected.to_csv(exit_path, sep=',', index=False)
    print('Le fichier', file_name + '_cleaned.csv a été exporté dans output')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ce script nettoie une courbe de charge CSV')
    parser.add_argument('--input_csv', '-i', type=str, required=True,
                          help='Fichier CSV en entrée. Doit contenir des colonnes nommées "Horodate" et "Valeur"')
    parser.add_argument('--timestep', '-t', type=int, default=60,
                        help='Pas de temps en minutes du CSV en sortie. Defaut : 60 minutes')

    args = parser.parse_args()

    main(args.input_csv, args.timestep)
