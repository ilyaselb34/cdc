import pandas as pd
import locale
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration locale pour les noms de jours en français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Chargement et préparation des données
file_name = 'output/Enedis_SGE_HDM_A0622Acleaned.csv'
data = pd.read_csv(file_name, sep=',')
data['date'] = pd.to_datetime(data['date'])
data['puissance_w'] /= 1000  # Convertir la puissance en kWh

# Préparation des données hebdomadaires
data_week = data.groupby(data['date'].dt.date)['puissance_w'
                                               ].sum().reset_index()
data_week['date'] = pd.to_datetime(data_week['date'])
data_week['jour_semaine'] = data_week['date'].dt.strftime('%A')

# Préparation des données mensuelles
data_month = data.groupby(data['date'].dt.to_period('M'))['puissance_w'
                                                          ].sum().reset_index()
data_month['date'] = data_month['date'].dt.to_timestamp()
data_month['mois'] = data_month['date'].dt.strftime('%B %Y')
data_month['energie_kWh'] = data_month['puissance_w']

palette = sns.color_palette("husl", len(data_month))

# Création de la figure avec deux sous-graphiques
fig, axes = plt.subplots(1, 2, figsize=(18, 8))

# Sous-graphique 1 : Boxplot de la consommation de puissance
# par jour de la semaine
sns.boxplot(ax=axes[0], x='jour_semaine', y='puissance_w', data=data_week,
            order=['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi',
                   'dimanche'])
sns.stripplot(ax=axes[0], x='jour_semaine', y='puissance_w', data=data_week,
              color='black', alpha=0.5, jitter=True,
              order=['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi',
                     'samedi', 'dimanche'])
axes[0].set_xlabel('Jour de la semaine')
axes[0].set_ylabel('Puissance (kWh)')
axes[0].set_title('Boxplot de la consommation de puissance par jour de '
                  'la semaine')

# Sous-graphique 2 : Diagramme en barres de la consommation mensuelle
axes[1].bar(data_month['mois'], data_month['energie_kWh'], color=palette)
axes[1].set_xlabel('Mois')
axes[1].set_ylabel('Consommation mensuelle (kWh)')
axes[1].set_title('Consommation mensuelle d\'énergie')
axes[1].tick_params(axis='x', rotation=45)

# Ajuster l'espacement entre les sous-graphiques
plt.tight_layout()

# Afficher la figure
plt.savefig('plots/A06GKIR0_combined.png')
plt.show()
