"""
Auteur : Ilyas El Boujadaini

Contenu : Création de données simulées(2 colonnes, une date et une valeur de charge prise aléatoirement dans un tableau) puis export au format csv
"""

#on génère un fichier csv à l'aide de python pour créer des données simulées avec un pas de temps régulier

#import des librairies nécessaires
import os   #pour les chemins
import sys #pour les chemins

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
path_repo = str(os.path.dirname(current_dir))

import datetime as dt #pour les dates
from random import * #pour les valeurs de charges aléatoires
import csv #pour l'export



def create_const_csv_data(start_time: dt.datetime, end_time: dt.datetime, time_step: int, data: list):
    """Generates a csv file with a constant time step(in minutes) for a year with random charge values

    Args:
        start_time (datetime): start time of the simulation
        end_time (datetime): end time of the simulation
        time_step (int): time step in minutes
        data (list): list of charge values
    
    Returns:
        None
    """
    simul=[]
    time=start_time
    while time<end_time:
        line=[time,data[randint(0,len(data)-1)]]
        simul.append(line)
        time += dt.timedelta(minutes=time_step)

    output_path = os.path.join('..', 'output', '00_simulation_' + str(time_step) +'min_const.csv')
    with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerows(simul)

data=[1000,2000,4000,5000,6000]
start_time = dt.datetime(2023,1,1)
end_time = dt.datetime(2024,1,1)
create_const_csv_data(start_time=start_time, end_time=end_time, time_step=10, data=data)