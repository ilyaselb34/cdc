"""
Author: Ilyas El Boujadaini

Content: Visualization of the average power profile per hour for each day
         of the week using a line graph.
"""

import pandas as pd
import locale
import matplotlib.pyplot as plt
import re
import os

# Set locale for day names in French
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# File path
file_name = r'output\Enedis_SGE_HDM_A06GKIR0_cleaned.csv'

# Load data
data = pd.read_csv(file_name, sep=',')
data['date'] = pd.to_datetime(data['date'])
data['puissance_kw'] = data['puissance_w'] / 1000

# Extract the day of the week in French
data['jour_semaine'] = data['date'].dt.strftime('%A')
data['heure'] = data['date'].dt.strftime('%H:%M:%S')

# Group the data by 'jour_semaine' and 'heure' columns and calculate the mean
# of 'puissance_w'
weekly_data = data.groupby(['jour_semaine', 'heure'])[
    'puissance_kw'].mean().reset_index()
mean_data = weekly_data.groupby('heure')['puissance_kw'].mean().reset_index()

pattern = r'Enedis_SGE_HDM_(.*?)_cleaned\.csv'

# Recherche de la correspondance dans la chaîne
match = re.search(pattern, file_name)

if match:
    # Extraire la partie correspondante
    result = match.group(1)
    # Créer le chemin de sortie avec le texte extrait
    exit_path = os.path.join('plots', result + '_profil_puissance_jour' +
                             + '.png')
else:
    exit_path = 'No match found'

# Définir les dates de début et de fin
date1 = data['date'].min().strftime('%d/%m/%Y')
date2 = data['date'].max().strftime('%d/%m/%Y')

# Create a figure and axis
plt.figure(figsize=(12, 8))
ax = plt.subplot(111)

# Define colors for each day of the week
colors = ['red', 'orange', 'yellow', 'pink', 'purple', 'cyan', 'blue']

# Iterate over each day of the week
for i, day in enumerate(['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi',
                         'samedi', 'dimanche']):
    # Filter data for the current day
    day_data = weekly_data[weekly_data['jour_semaine'] == day]
    # Plot the points and connect them with lines
    ax.plot(day_data['heure'], day_data['puissance_kw'],
            linestyle='-', color=colors[i], label=day)

# Plot mean_data with thicker black line
ax.plot(mean_data['heure'], mean_data['puissance_kw'], color='black',
        linestyle='-', linewidth=4, label='Moyenne Générale')

# Set labels and title
plt.xlabel('Heure')
plt.ylabel('Puissance Moyenne (kW)')
plt.title(f'Profil de la Puissance Moyenne par Heure pour Chaque Jour de '
          'la Semaine\n'
          f'Ce graphique concerne des valeurs récoltées du {date1} au {date2}')
plt.xticks(rotation=45)
plt.grid(True)

# Add legend
plt.legend()

# Save and show the plot
plt.tight_layout()
plt.savefig(exit_path)
plt.show()
