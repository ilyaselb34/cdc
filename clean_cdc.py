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


def main(file_name: str, timestep: int, output_dir: str):

    # The file address may contain backslashes, we need to escape them
    file_name = file_name.replace('\\', '\\\\')
    delimiter = dlmt.detect_delimiter(file_name)

    # Load data with the correct encoding
    data = pd.read_csv(file_name, sep=delimiter)
    data['date'] = pd.to_datetime(data['Horodate'].str.split('+').str[0])
    data['puissance_w'] = data['Valeur']

    del data['Valeur']
    del data['Horodate']

    date_min = data['date'].min().strftime('%d/%m/%Y')
    date_max = data['date'].max().strftime('%d/%m/%Y')
    etendue = (data['date'].max() - data['date'].min()).days
    print(f'\n\n\nFichier: {file_name}\n'
          f'Date min: {date_min}\n'
          f'Date max: {date_max}\n'
          f'Etendue: {etendue} jours\n\n\n')

    # on bouche les trous de données brutes:
    # soit par interpolation linéaire(moins de 4h)
    # soit par moyenne mobile(plus de 4h)
    data_corrected = crct.dataset_correction(data, timestep)

    # sert à vérifier la continuité de l'écart entre les mesures corrigées
    data_corrected['pas_temps'] = [0] + (data_corrected['date'].diff()
                                         / pd.Timedelta(minutes=1)).fillna(0)
    step_change = data_corrected[data_corrected['pas_temps']
                                 != data_corrected['pas_temps'].shift()]
    print('Ce tableau vérifie si des écarts de temps subsistent entre les '
          'mesures')
    print(step_change, '\n\n\n')

    # On récupère le nom du fichier sans le chemin
    prefix = os.path.splitext(os.path.basename(file_name))[0]

    # si dossier d'export non précisé, on prend le nom du fichier
    if output_dir is None:
        output_dir = prefix
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Export du CSV nettoyé
    output_csv = os.path.join(output_dir, prefix + '_cleaned.csv')
    data_corrected.to_csv(output_csv, sep=',', index=False)

    # Load data
    data = data_corrected

    # Extract dates without time and additional columns
    data['date_sans_heure'] = data['date'].dt.date
    data['puissance_kw'] = data['puissance_w'] / 1000

    # Profil journalier
    output_png = os.path.join(output_dir, prefix + '_profil_journalier.png')
    pt.lineplot_profil_journalier(data, output_png, date_min, date_max)

    # Profil hebdomadaire
    output_png = os.path.join(output_dir, prefix + '_profil_hebdo.png')
    pt.boxplot_profil_hebdo(data, output_png, date_min, date_max)

    # Profil annuel
    output_png = os.path.join(output_dir, prefix + '_profil_annuel.png')
    pt.barplot_profil_annuel(data, output_png, date_min, date_max)

    print(f'Graphiques exportés dans le dossier {output_dir}\n\n\n')


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
                        help='Nom du répertoire exporté. Par défaut, prend le'
                        'même nom que le CSV en entrée.')

    args = parser.parse_args()

    main(args.input_csv, args.timestep, args.output_dir)
