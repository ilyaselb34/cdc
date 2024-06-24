"""
Author: Ilyas El Boujadaini

Content: Visualization of the monthly consumption using a barplot.
"""

import pandas as pd
import locale
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

# Set locale for day names in French
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    print("La locale 'fr_FR.UTF-8' n'est pas installée sur ce système.")


# Assign the month name in French based on the month number
def assign_month_name(month_num):
    months_fr = {
        1: 'janvier',
        2: 'février',
        3: 'mars',
        4: 'avril',
        5: 'mai',
        6: 'juin',
        7: 'juillet',
        8: 'août',
        9: 'septembre',
        10: 'octobre',
        11: 'novembre',
        12: 'décembre'
    }
    return months_fr.get(month_num, 'inconnu')


# File path
file_name = 'output/Enedis_SGE_HDM_A06GKIR0_cleaned.csv'
data = pd.read_csv(file_name, sep=',')
data['date'] = pd.to_datetime(data['date'])

# Créer deux nouvelles colonnes: mois et nom_mois
data['mois'] = data['date'].dt.month
data['nom_mois'] = data['mois'].map(assign_month_name
                                    ) + ' ' + data['date'].dt.year.astype(str)
data['mois_annee'] = data['date'].dt.strftime('%Y-%m')

# Grouper les données par mois et année
grouped_data = data.groupby('mois_annee')
somme_puissance_par_mois = grouped_data['puissance_w'].sum().reset_index()

# Ajouter la colonne nom_mois
data_month = somme_puissance_par_mois.merge(
    data[['mois_annee', 'nom_mois']].drop_duplicates(),
    on='mois_annee',
    how='left'
)

# Convert power to kWh
data_month['energie_kwh'] = data_month['puissance_w'] / 1000
del data_month['puissance_w']

# Add a column to color the bars according to the season
data_month['couleur'] = 'blue'
data_month.loc[data_month['mois_annee'].str.contains('-03|-04|-05'), 'couleur'
               ] = 'green'
data_month.loc[data_month['mois_annee'].str.contains('-06|-07|-08'), 'couleur'
               ] = 'yellow'
data_month.loc[data_month['mois_annee'].str.contains('-09|-10|-11'), 'couleur'
               ] = 'orange'

print(data_month)

pattern = r'Enedis_SGE_HDM_(.*?)_cleaned\.csv'

# Recherche de la correspondance dans la chaîne
match = re.search(pattern, file_name)

if match:
    # Extraire la partie correspondante
    result = match.group(1)
    # Créer le chemin de sortie avec le texte extrait
    exit_path = os.path.join('plots', result + '_profil_annuel_mois.png')
else:
    exit_path = 'No match found'

# Définir les dates de début et de fin
date1 = data['date'].min().strftime('%d/%m/%Y')
date2 = data['date'].max().strftime('%d/%m/%Y')

# Create a bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x='nom_mois', y='energie_kwh', data=data_month, palette=data_month[
    'couleur'].tolist())
plt.xlabel('Mois')
plt.ylabel('Energie (kWh)')
plt.title(f'Consommation par jour de la semaine\n'
          f'Ce graphique concerne des valeurs récoltées du {date1} au {date2}')

# Ajouter la légende manuellement
import matplotlib.patches as mpatches
handles = [
    mpatches.Patch(color='green', label='Printemps'),
    mpatches.Patch(color='yellow', label='Été'),
    mpatches.Patch(color='orange', label='Automne'),
    mpatches.Patch(color='blue', label='Hiver')
]
plt.legend(handles=handles, title='Saison')
plt.savefig(exit_path)

plt.show()
