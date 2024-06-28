#!/usr/bin/env python

import argparse
import locale
import os
import pandas as pd
import sys

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

current_dir = os.path.dirname(os.path.abspath(__file__))
tools_dir = os.path.join(current_dir, 'tools')
sys.path.append(tools_dir)
import correction as crct  # type: ignore
import delimiter as dlmt  # type: ignore
import plot_tools as pt  # type: ignore


# Set locale for day names in French
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    print("La locale 'fr_FR.UTF-8' n'est pas installée sur ce système.")


def main(file_name: str, timestep: int):

    # The file address may contain backslashes, we need to escape them
    file_name = file_name.replace('\\', '\\\\')
    delimiter = dlmt.detect_delimiter(file_name)

    # Load data with the correct encoding
    data = pd.read_csv(file_name, sep=delimiter, header=2)
    data['date'] = pd.to_datetime(data['Horodate'].str.split('+').str[0],
                                  format="%Y-%m-%dT%H:%M:%S")
    data['puissance_w'] = data['Valeur']

    del data['Valeur']
    del data['Horodate']

    date1 = data['date'].min().strftime('%d/%m/%Y')
    date2 = data['date'].max().strftime('%d/%m/%Y')
    print(f'Le fichier {file_name} contient des données mesurées entre le',
          f'{date1} et {date2}.\n\n\n')

    data_corrected = crct.dataset_correction(data, timestep)
    data_corrected['pas_temps'] = [0] + (data_corrected['date'].diff()
                                         / pd.Timedelta(minutes=1)).fillna(0)
    step_change = data_corrected[data_corrected['pas_temps']
                                 != data_corrected['pas_temps'].shift()]
    print('Le tableau suivant montre si il y a une variation du pas temporel')
    print(step_change, '\n\n\n')

    # On récupère le nom du fichier sans le chemin
    prefix = os.path.splitext(os.path.basename(file_name))[0]

    exit_path = os.path.join('output', prefix + '_cleaned.csv')

    data_corrected.to_csv(exit_path, sep=',', index=False)
    print('Le fichier', file_name + '_cleaned.csv a été exporté dans output')

    # Load data
    data = data_corrected

    # Extract dates without time and additional columns
    data['date_sans_heure'] = data['date'].dt.date
    data['puissance_kw'] = data['puissance_w'] / 1000

    pt.boxplot(data, prefix, date1, date2)
    pt.barplot(data, prefix, date1, date2)
    pt.lineplot(data, prefix, date1, date2)

    if output_dir == None:
        output_dir = prefix

    pt.boxplot(data, prefix, date1, date2)
    pt.barplot(data, prefix, date1, date2)
    pt.lineplot(data, prefix, date1, date2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ce script nettoie une courbe'
                                     'de charge CSV')
    parser.add_argument('--input_csv', '-i', type=str, required=True,
                        help='Fichier CSV en entrée. Doit contenir des'
                        'colonnes nommées "Horodate" et "Valeur"')
    parser.add_argument('--timestep', '-t', type=int, default=60,
                        help='Pas de temps en minutes du CSV en sortie.'
                        'Defaut : 60 minutes')
    parser.add_argument('--output_dir', '-o', type=str, default=None,
                        help='Nom du répertoire exporté. Par défaut, prend le même nom que le CSV en entrée.')

    args = parser.parse_args()

    main(args.input_csv, args.timestep, args.output_dir)