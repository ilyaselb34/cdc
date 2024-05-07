"""
Auteur : Ilyas El Boujadaini

Contenu : Analyse des données simulées (calcul de la moyenne de charge par jour)
"""

#import des librairies nécessaires

import csv  #pour l'import et l'export de données
import pandas as pd #pour les dataframes
import datetime as dt   #pour les dates
import os   #pour les chemins

entry_path = os.path.join('..', 'output', '00_simulation_5_min_const.csv') #chemin du fichier de données simulées, adaptation à l'os de l'utilisateur
simul=[]    #liste qui accueillera les données

with open(entry_path, "r", newline='', encoding='utf-8') as fichier_csv:    #ouverture du fichier
    lecteur_csv = csv.reader(fichier_csv, delimiter=";")
    for ligne in lecteur_csv:
            ligne[0]=dt.datetime.strptime(ligne[0], '%Y-%m-%d %H:%M:%S')   #conversion de la date en format datetime
            ligne[1]=int(ligne[1])  #conversion de la charge en entier pour les moyennes
            simul.append(ligne)

def moyenne_charge_jour(simul):
    df=pd.DataFrame(simul,columns=['date','charge'])   #création d'un dataframe pour faciliter les calculs
    moyenne_jour = df.groupby(df['date'].dt.date)['charge'].mean().reset_index()   #calcul de la moyenne de charge par jour
    return moyenne_jour

res=moyenne_charge_jour(simul)
print(res.head(5))

exit_path = os.path.join('..', 'output', '01_simulation_analysis.csv')
res.to_csv(exit_path, sep=';', index=False, header=False, encoding='utf-8')