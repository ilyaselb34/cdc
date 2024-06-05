import pandas as pd
import locale
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

file_name = 'output/Enedis_SGE_HDM_A06GKIR0_cleaned.csv'
data = pd.read_csv(file_name, sep=',')
data['date'] = pd.to_datetime(data['date'])
data['puissance_w'] /= 1000
data = data.groupby(data['date'].dt.date)['puissance_w'].sum().reset_index()
data['date'] = pd.to_datetime(data['date'])
data['jour_semaine'] = data['date'].dt.strftime('%A')

plt.figure(figsize=(12, 6))
sns.boxplot(x='jour_semaine', y='puissance_w', data=data, order=[
    'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'])
plt.xlabel('Jour de la semaine')
plt.ylabel('Puissance (kWh)')
plt.title('Boxplot de la consommation de puissance par jour de la semaine')
plt.savefig('plots/A06GKIR0_daily_mean.png')
plt.show()
