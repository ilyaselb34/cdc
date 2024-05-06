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
print(jours.head(5))
print('le nb de jours est',len(jours))