"""
Author: Ilyas El Boujadaini

Content: Correction of the whole dataset.
"""

import locale
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import sys

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tools_dir = os.path.join(parent_dir, 'tools')
sys.path.append(tools_dir)
import correction as crct  # type: ignore
import delimiter as dlmt  # type: ignore
import plot_tools as pt  # type: ignore


# Initializes the path to the csv file, adapting it to the user's OS
file_name = 'C:\Users\ily_y\OneDrive\Bureau\L3 MIASHS\stage\cdc\input\Enedis_SGE_HDM_A06GKKU4.csv'
file_name = os.path.normpath(file_name)

delimiter = dlmt.detect_delimiter(file_name)
data = pd.read_csv(file_name, sep=delimiter, header=2)
data['date'] = pd.to_datetime(data['Horodate'].str.split('+').str[0],
                              format="%Y-%m-%dT%H:%M:%S")
del data['Horodate']
data['puissance_w'] = data['Valeur']
del data['Valeur']

# We call the main function, verify the time step between each data point and
# export the final result in a csv file

data_corrected = crct.dataset_correction(data, 60)
data_corrected['jour_semaine'] = data_corrected['date'].dt.strftime('%A')
data_corrected['pas_temps'] = [0] + (data_corrected['date'].diff()
                                     / pd.Timedelta(minutes=1)).fillna(0)
step_change = data_corrected[data_corrected['pas_temps']
                             != data_corrected['pas_temps'].shift()]
print('Le tableau suivant montre si il y a une variation du pas temporel')
print(step_change, '\n\n\n')

pattern = r'(Enedis.*?\.csv)'
match = re.search(pattern, file_name)
result = match.group(1)
exit_path = os.path.join('output', result[:-4] + '_cleaned.csv')

data_corrected.to_csv(exit_path, sep=',', index=False)
print('Le fichier', file_name + '_cleaned.csv a été exporté dans output')

# Load data
data = data_corrected

# Extract dates without time and additional columns
data['date_sans_heure'] = data['date'].dt.date
data['puissance_kw'] = data['puissance_w'] / 1000

# Group data by date without time
grouped_data = data.groupby('date_sans_heure')

# Calculate the sum of 'puissance_w' for each group
somme_puissance_par_date = grouped_data['puissance_w'].sum()

# Reset the index to get a DataFrame
data_week = somme_puissance_par_date.reset_index()

# Convert 'date_sans_heure' to datetime type
data_week['date'] = pd.to_datetime(data_week['date_sans_heure'])

# Extract the day of the week in French
data_week['jour_semaine'] = data_week['date'].dt.strftime('%A')
data_week['energie_kwh'] = data_week['puissance_w'] / 1000

date1 = data_week['date'].min().strftime('%d/%m/%Y')
date2 = data_week['date'].max().strftime('%d/%m/%Y')


# Apply the function to the 'date' column to create the 'couleur' column
data_week['couleur'] = data_week['date'].apply(pt.get_season_color)

del data_week['date_sans_heure']
del data_week['puissance_w']

print(data_week.head())

pattern = r'Enedis_SGE_HDM_(.*?)\.csv'

# Search for the match in the string
match = re.search(pattern, file_name)

if match:
    # Extract the corresponding part
    result = match.group(1)
else:
    result = 'No match found'

# Plot 1: Boxplot Journalier
exit_path1 = os.path.join('plots', result + '_boxplot_journalier.png')
plt.figure(figsize=(12, 6))
sns.boxplot(x='jour_semaine', y='energie_kwh', data=data_week,
            showfliers=False, order=['lundi', 'mardi', 'mercredi', 'jeudi',
                                     'vendredi', 'samedi', 'dimanche'],
            color='white')

for color in data_week['couleur'].unique():
    sns.stripplot(x='jour_semaine', y='energie_kwh',
                    data=data_week[data_week['couleur'] == color],
                    color=color, alpha=0.5, jitter=True,
                    order=['lundi', 'mardi', 'mercredi', 'jeudi',
                           'vendredi', 'samedi', 'dimanche'])

sns.pointplot(x='jour_semaine', y='energie_kwh', data=data_week,
                order=['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi',
                       'samedi', 'dimanche'], estimator=np.mean,
                errorbar=None, color='red', markers='D', linestyles='',
                label='Moyenne')

handles, labels = plt.gca().get_legend_handles_labels()
handles.append(plt.Line2D([0], [0], marker='o', color='w',
                          label='Données Individuelles',
                          markerfacecolor='black', markersize=10))
plt.legend(handles=handles)
plt.xlabel('Jour de la semaine')
plt.ylabel('Consommation Journalière (kWh)')
plt.title(f'Consommation par jour de la semaine\n'
          f'Ce graphique concerne des valeurs récoltées du {date1} au {date2}')
plt.savefig(exit_path1)

# Plot 2: Profil Annuel Mensuel
data['mois'] = data['date'].dt.month
data['nom_mois'] = data['mois'].map(pt.assign_month_name) + ' ' + data[
    'date'].dt.year.astype(str)
data['mois_annee'] = data['date'].dt.strftime('%Y-%m')

grouped_data = data.groupby('mois_annee')
somme_puissance_par_mois = grouped_data['puissance_w'].sum().reset_index()

data_month = somme_puissance_par_mois.merge(
    data[['mois_annee', 'nom_mois']].drop_duplicates(),
    on='mois_annee',
    how='left'
)

data_month['energie_kwh'] = data_month['puissance_w'] / 1000
del data_month['puissance_w']

data_month['couleur'] = 'blue'
data_month.loc[data_month['mois_annee'].str.contains('-03|-04|-05'),
               'couleur'] = 'green'
data_month.loc[data_month['mois_annee'].str.contains('-06|-07|-08'),
               'couleur'] = 'yellow'
data_month.loc[data_month['mois_annee'].str.contains('-09|-10|-11'),
               'couleur'] = 'orange'

exit_path2 = os.path.join('plots', result + '_profil_annuel_mois.png')

plt.figure(figsize=(10, 6))
sns.barplot(x='nom_mois', y='energie_kwh', data=data_month, palette=data_month[
    'couleur'].tolist())
plt.xlabel('Mois')
plt.ylabel('Energie (kWh)')
plt.title(f'Consommation par mois\n'
          f'Ce graphique concerne des valeurs récoltées du {date1} au {date2}')


handles = [
    mpatches.Patch(color='green', label='Printemps'),
    mpatches.Patch(color='yellow', label='Été'),
    mpatches.Patch(color='orange', label='Automne'),
    mpatches.Patch(color='blue', label='Hiver')
]
plt.legend(handles=handles, title='Saison')
plt.savefig(exit_path2)

# Plot 3: Profil de Puissance Journalière
data['jour_semaine'] = data['date'].dt.strftime('%A')
data['heure'] = data['date'].dt.strftime('%H:%M:%S')

weekly_data = data.groupby(['jour_semaine', 'heure'])[
    'puissance_kw'].mean().reset_index()
mean_data = weekly_data.groupby('heure')['puissance_kw'].mean().reset_index()

exit_path3 = os.path.join('plots', result + '_profil_puissance_jour.png')

plt.figure(figsize=(12, 8))
ax = plt.subplot(111)

colors = ['red', 'orange', 'yellow', 'pink', 'purple', 'cyan', 'blue']

for i, day in enumerate(['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi',
                        'samedi', 'dimanche']):
    day_data = weekly_data[weekly_data['jour_semaine'] == day]
    ax.plot(day_data['heure'], day_data['puissance_kw'],
            linestyle='-', color=colors[i], label=day)

ax.plot(mean_data['heure'], mean_data['puissance_kw'], color='black',
        linestyle='-', linewidth=4, label='Moyenne Générale')

plt.xlabel('Heure')
plt.ylabel('Puissance Moyenne (kW)')
plt.title(f'Profil de la Puissance Moyenne par Heure pour Chaque Jour de '
          'la Semaine\n'
          f'Ce graphique concerne des valeurs récoltées du {date1} au {date2}')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(exit_path3)
