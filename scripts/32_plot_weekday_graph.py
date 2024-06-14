import pandas as pd
import locale
import matplotlib.pyplot as plt

# Set locale for day names in French
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# File path
file_name = r'output\Enedis_SGE_HDM_A06229H0_cleaned.csv'

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
plt.title('Profil de la Puissance Moyenne par Heure pour Chaque Jour de'
          'la Semaine')
plt.xticks(rotation=45)
plt.grid(True)

# Add legend
plt.legend()

# Save and show the plot
plt.tight_layout()
plt.savefig('plots/progil_puissance.png')
plt.show()
