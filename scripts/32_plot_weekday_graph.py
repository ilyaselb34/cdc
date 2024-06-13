import pandas as pd
import locale
import matplotlib.pyplot as plt
import seaborn as sns

# Set locale for day names in French
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# File path
file_name = r'output\Enedis_SGE_HDM_A06229H0_cleaned.csv'

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

del data_week['date_sans_heure']
del data_week['puissance_w']

print(data_week.head(20))

# Define the order of days in French
jours_semaine_order = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi',
                       'samedi', 'dimanche']

# Convert 'jour_semaine' to a categorical type with the specified order
data_week['jour_semaine'] = pd.Categorical(
    data_week['jour_semaine'], categories=jours_semaine_order, ordered=True)

# Plotting the graph
plt.figure(figsize=(12, 8))

# Use seaborn to plot the data
sns.lineplot(data=data_week, x='date', y='energie_kwh', hue='jour_semaine',
             marker='o', hue_order=jours_semaine_order)

# Set plot title and labels
plt.title(f"Consommation d'énergie (kWh) par jour de la semaine\n"
          f"Du {date1} au {date2}")
plt.xlabel('Date')
plt.ylabel('Énergie (kWh)')
plt.legend(title='Jour de la semaine')
plt.grid(True)

# Show the plot
plt.show()
