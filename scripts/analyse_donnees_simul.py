import csv
import pandas as pd
from datetime import datetime, timedelta
from math import *
import numpy as np

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
    
simul=lecture_fichier_csv("simulation.csv",";",'utf-8',0)
df=pd.DataFrame(simul,columns=['date','charge'])
jours=df[df['date'].dt.hour == 0]
def moyenne_charge_jour(simul):
    sortie=[]
    df=pd.DataFrame(simul,columns=['date','charge'])
    jours=df[df['date'].dt.hour == 0]
    print(df[df['date'] == df['date'][0]]['charge'].mean())
    for i in jours['date']:
        moyenne_jour=df[df['date'] == i]['charge'].mean()
        sortie.append([i,moyenne_jour])
    return sortie
res=moyenne_charge_jour(simul)
print(res[:20])
with open('analyse_simulation.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';')
        writer.writerows(res)
