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
    df = pd.read_csv(file_name, sep=delimiter)
    df['date'] = pd.to_datetime(df['Horodate'].str.split('+').str[0])
    df['puissance_w'] = df['Valeur']

    # del data['Valeur']
    # del data['Horodate']

    # Petit echo pour faire un résumé des données
    date_min = df['date'].min().strftime('%d/%m/%Y')
    date_max = df['date'].max().strftime('%d/%m/%Y')
    etendue = (df['date'].max() - df['date'].min()).days
    print(f'Début: {date_min}; Fin: {date_max}; Etendue: {etendue}j')

    # On corrige les données brutes en "bouchant les trous" :
    # Par interpolation linéaire, quand le trou estcelui-ci est <4h
    # Par moyenne mobile, quand celui-ci est >4h
    df = crct.dataset_correction(df, timestep)

    # sert à vérifier la continuité de l'écart entre les mesures corrigées
    df['timestep'] = [0] + (df['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    df_check_timestep = df[df['timestep'] != df['timestep'].shift()]
    print('Ce tableau vérifie si des écarts de temps subsistent entre les mesures')
    print(df_check_timestep, '\n')

    # On récupère le nom du fichier sans le chemin
    prefix = os.path.splitext(os.path.basename(file_name))[0]

    # si dossier d'export non précisé, on prend le nom du fichier
    if output_dir is None:
        output_dir = prefix
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # On exporte le fichier CSV nettoyé
    output_csv = os.path.join(output_dir, prefix + '_cleaned.csv')
    df.to_csv(output_csv, sep=',', index=False)

    # Extract dates without time and additional columns
    df['date_sans_heure'] = df['date'].dt.date
    df['puissance_kw'] = df['puissance_w'] / 1000

    # Profil journalier
    output_png = os.path.join(output_dir, prefix + '_profil_journalier.png')
    pt.lineplot_profil_journalier(df, output_png, date_min, date_max)

    # Profil hebdomadaire
    output_png = os.path.join(output_dir, prefix + '_profil_hebdo.png')
    pt.boxplot_profil_hebdo(df, output_png, date_min, date_max)

    # Profil annuel
    output_png = os.path.join(output_dir, prefix + '_profil_annuel.png')
    pt.barplot_profil_annuel(df, output_png, date_min, date_max)

    print(f'Les graphiques ont été exportés dans le dossier {output_dir}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ce script nettoie une courbe'
                                     'de charge CSV et exporte 3 graphiques')
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
