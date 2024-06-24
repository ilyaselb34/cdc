"""
Author: Ilyas El Boujadaini

Content: Visualization of the daily consumption by day of the week using a
         boxplot.
"""
import pandas as pd
import locale
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
import os

# Set locale for day names in French
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# File path
file_name = r'output\Enedis_SGE_HDM_A06GKIR0_cleaned.csv'

# Load data
data = pd.read_csv(file_name, sep=',')
data['date'] = pd.to_datetime(data['date'])
data['puissance_w']  # Convert power to kWh

# Extract dates without time
data['date_sans_heure'] = data['date'].dt.date

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


# Define a function to determine the season color based on the date
def get_season_color(date):
    year = date.year
    spring = pd.Timestamp(f'{year}-03-21')
    summer = pd.Timestamp(f'{year}-06-21')
    autumn = pd.Timestamp(f'{year}-09-21')
    winter = pd.Timestamp(f'{year}-12-21')

    if spring <= date < summer:
        return 'green'  # Spring
    elif summer <= date < autumn:
        return 'yellow'  # Summer
    elif autumn <= date < winter:
        return 'orange'  # Autumn
    else:
        return 'blue'  # Winter


# Apply the function to the 'date' column to create the 'couleur' column
data_week['couleur'] = data_week['date'].apply(get_season_color)

del data_week['date_sans_heure']
del data_week['puissance_w']

print(data_week.head())

pattern = r'Enedis_SGE_HDM_(.*?)_cleaned\.csv'

# Search for the match in the string
match = re.search(pattern, file_name)

if match:
    # Extract the corresponding part
    result = match.group(1)
    # Create the output path with the extracted text
    exit_path = os.path.join('plots', result + '_boxplot_journalier.png')
else:
    exit_path = 'No match found'

# Create the plot
plt.figure(figsize=(12, 6))
sns.boxplot(x='jour_semaine', y='energie_kwh', data=data_week,
            showfliers=False, order=['lundi', 'mardi', 'mercredi', 'jeudi',
                                     'vendredi', 'samedi', 'dimanche'],
            color='white')

# Plot the stripplot with the individual colors
for color in data_week['couleur'].unique():
    sns.stripplot(x='jour_semaine', y='energie_kwh',
                  data=data_week[data_week['couleur'] == color],
                  color=color, alpha=0.5, jitter=True,
                  order=['lundi', 'mardi', 'mercredi', 'jeudi',
                         'vendredi', 'samedi', 'dimanche'])

sns.pointplot(x='jour_semaine', y='energie_kwh', data=data_week,
              order=['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi',
                     'samedi', 'dimanche'], estimator=np.mean, errorbar=None,
              color='red', markers='D', linestyles='', label='Moyenne')

# Add a handle for individual points in the legend
handles, labels = plt.gca().get_legend_handles_labels()
handles.append(plt.Line2D([0], [0], marker='o', color='w',
                          label='Données Individuelles',
                          markerfacecolor='black', markersize=10))
plt.legend(handles=handles)
plt.xlabel('Jour de la semaine')
plt.ylabel('Consommation Journalière (kWh)')
plt.title(f'Consommation par jour de la semaine\n'
          f'Ce graphique concerne des valeurs récoltées du {date1} au {date2}')
plt.savefig(exit_path)
plt.show()
