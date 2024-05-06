import csv
import pandas as pd
from datetime import datetime, timedelta
from math import *
import numpy as np
import os
import sys

def lecture_fichier_csv( nom_fichier, delimitateur, encodage, nb_lignes_entete):
    try:
        fichier = open(nom_fichier,"r", encoding=encodage)
        cr = csv.reader(fichier,delimiter = delimitateur)

        for i in range(nb_lignes_entete):
            cr.__next__()   # Spécificité Python permettant de passer
                            #à la ligne suivante du csv

        resultat = []
        for ligne in cr:
            ligne[0]=datetime.strptime(ligne[0], '%Y-%m-%d %H:%M:%S')
            ligne[1]=int(ligne[1])
            resultat.append(ligne)

        fichier.close()
        return resultat
    except:
        return []

chemin_fichier = os.path.join('..', 'output', 'simulation.csv')
simul=lecture_fichier_csv(chemin_fichier,";",'utf-8',0)
def moyenne_charge_jour(simul):
    df=pd.DataFrame(simul,columns=['date','charge'])
    moyenne_jour = df.groupby('date')['charge'].mean()
    return moyenne_jour
res=moyenne_charge_jour(simul)
print(res.head(5))
chemin_fichier = os.path.join('..', 'output', 'analyse_simulation.csv')
with open(chemin_fichier, 'w', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';')
        writer.writerows(res)
