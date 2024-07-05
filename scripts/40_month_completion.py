"""
Author: Ilyas El Boujadaini

Content: Completion of missing months in the cleaned data set.
"""
import pandas as pd
import locale
import datetime as dt

# Set locale for day names in French
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    print("La locale 'fr_FR.UTF-8' n'est pas installée sur ce système.")

# File path
file_name = r'Enedis_SGE_HDM_A06229H0\Enedis_SGE_HDM_A06229H0_cleaned.csv'

# Load data with the correct encoding
data = pd.read_csv(file_name, sep=',', encoding='utf-8')
data['date'] = pd.to_datetime(data['date'])
data['puissance_kwh'] = data['puissance_w'] / 1000
del data['puissance_w']

date_min = data['date'].min()
date_max = data['date'].max()
print(date_max + dt.timedelta(days=1))
print(f'Le fichier {file_name} contient des données mesurées entre le',
      f'{date_min} et {date_max}.\n\n\n')

data['jour_semaine'] = data['date'].dt.weekday
print(data.head())
data['heure'] = data['date'].dt.strftime('%H')
grouped_data = data.groupby(['jour_semaine', 'heure'])

# on sort un tableau pour chaque heure de la semaine (moyenne de la puissance)
# nommé djh (pour date_jour_heure)
djh = grouped_data['puissance_kwh'].mean().reset_index()

# année de référence de l'étude
year = date_min.year
start_day = dt.datetime(year - 1, 12, 31)

date_min -= dt.timedelta(days=1)
while date_min > start_day:
    weekday = date_min.weekday()
    day = djh[djh['jour_semaine'] == weekday]

    res = pd.DataFrame(columns=['date', 'puissance_kwh', 'jour_semaine'])
    res['date'] = f'{year}-{date_min.month}-{date_min.day} ' + day['heure']
    res['date'] = pd.to_datetime(res['date'])
    res['puissance_kwh'] = day['puissance_kwh']
    res['jour_semaine'] = weekday
    res['type_valeur'] = 'Mois manquant'
    data = pd.concat([data, res], ignore_index=True)
    date_min -= dt.timedelta(days=1)

end_day = dt.datetime(year + 1, 1, 1)
date_max += dt.timedelta(days=1)
while date_max < end_day:
    weekday = date_max.weekday()
    day = djh[djh['jour_semaine'] == weekday]

    res = pd.DataFrame(columns=['date', 'puissance_kwh', 'jour_semaine'])
    res['date'] = f'{year}-{date_max.month}-{date_max.day} ' + day['heure']
    res['date'] = pd.to_datetime(res['date'])
    res['puissance_kwh'] = day['puissance_kwh']
    res['jour_semaine'] = weekday
    res['type_valeur'] = 'Mois manquant'
    data = pd.concat([data, res], ignore_index=True)
    date_max += dt.timedelta(days=1)

data.drop_duplicates(subset='date', keep='first', inplace=True)
data.sort_values(by='date', inplace=True)
data.to_csv('ehoe.csv', index=False, sep=',')
