import pandas as pd
import locale
import matplotlib.pyplot as plt
import seaborn as sns

# Set locale for day names in French
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# File path
file_name = 'output/Enedis_SGE_HDM_A06GKKU4_cleaned.csv'
data = pd.read_csv(file_name, sep=',')
data['date'] = pd.to_datetime(data['date'])

# Créer une nouvelle colonne avec le format mois et année
data['nom_mois'] = data['date'].dt.strftime('%B %Y')
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

# Ajouter la colonne energie_kwh
data_month['energie_kwh'] = data_month['puissance_w'] / 1000
del data_month['puissance_w']

# Ajouter une colonne couleur
data_month['couleur'] = 'blue'
data_month.loc[data_month['mois_annee'].str.contains('-03|-04|-05'), 'couleur'
               ] = 'green'
data_month.loc[data_month['mois_annee'].str.contains('-06|-07|-08'), 'couleur'
               ] = 'yellow'
data_month.loc[data_month['mois_annee'].str.contains('-09|-10|-11'), 'couleur'
               ] = 'orange'

print(data_month)

# Create a bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x='nom_mois', y='energie_kwh', data=data_month, palette=data_month[
    'couleur'].tolist())
plt.xlabel('Mois')
plt.ylabel('Energie (kWh)')
plt.title('Consommation d\'énergie par mois')

# Ajouter la légende manuellement
import matplotlib.patches as mpatches
handles = [
    mpatches.Patch(color='green', label='Printemps'),
    mpatches.Patch(color='yellow', label='Été'),
    mpatches.Patch(color='orange', label='Automne'),
    mpatches.Patch(color='blue', label='Hiver')
]
plt.legend(handles=handles, title='Saison')

plt.show()
