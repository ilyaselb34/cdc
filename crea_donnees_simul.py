"""
Auteur : Ilyas El Boujadaini

Contenu : Création de données simulées(2 colonnes, une date et une valeur de charge prise aléatoirement dans un tableau) puis export au format csv
"""
#on génère un fichier csv à l'aide de python pour
from datetime import datetime, timedelta #pour les dates
from random import * #pour les valeurs de charges aléatoires
import csv #pour l'export
exemple=[]#liste de départ
data=[1000,2000,4000,5000,6000]#valeurs possibles en watt
def create_csv_data(exemple,time_step):#exemple
    time=datetime(2023,1,1,0,0)
    for i in range(0,525600,time_step):
        line=[time,data[randint(0,len(data)-1)]]
        exemple.append(line)
        time += timedelta(minutes=time_step)
    with open('cdc/simulation.csv', 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerows(exemple)
create_csv_data(exemple,60)

