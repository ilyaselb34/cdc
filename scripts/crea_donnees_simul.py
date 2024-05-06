"""
Auteur : Ilyas El Boujadaini

Contenu : Création de données simulées(2 colonnes, une date et une valeur de charge prise aléatoirement dans un tableau) puis export au format csv
"""
#on génère un fichier csv à l'aide de python pour créer des données simulées avec un pas de temps régulier (60 minutes)
from datetime import datetime, timedelta #pour les dates
from random import * #pour les valeurs de charges aléatoires
import csv #pour l'export
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
path_repo = str(os.path.dirname(current_dir))

exemple=[]#liste de départ
data=[1000,2000,4000,5000,6000]#valeurs possibles en watt
def create_csv_data(exemple,time_step):#exemple: liste de départ, time_step: pas de temps(en minutes)
    time=datetime(2023,1,1,0,0)#utilisation du format datetime
    for i in range(0,525600,time_step):#boucle pour générer les données, 525600 minutes dans une année, le pas de temps détermine le nombre de lignes
        line=[time,data[randint(0,len(data)-1)]]#on attribue une valeur au hasard parmi les valeurs possibles
        exemple.append(line)#on ajoute la ligne à la liste
        time += timedelta(minutes=time_step)#on incrémente le temps en fonction du pas de temps
    chemin_fichier = os.path.join('..', 'output', 'simulation.csv')
    with open(chemin_fichier, 'w', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';')
        writer.writerows(exemple)

create_csv_data(exemple,60)#on appelle la fonction pour créer les données simulées