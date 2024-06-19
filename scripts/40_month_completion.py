"""
Author: Ilyas El Boujadaini

Content: Completion of missing months in the cleaned data set.
"""
import pandas as pd
import locale

# Set locale for day names in French
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    print("La locale 'fr_FR.UTF-8' n'est pas installée sur ce système.")

# File path
file_name = r'output\Enedis_SGE_HDM_A06229H0_cleaned.csv'

# Load data with the correct encoding
data = pd.read_csv(file_name, sep=',', encoding='utf-8')
data['date'] = pd.to_datetime(data['date'])


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


def days_number(month, year):
    months_fr = {
        'janvier': 31,
        'février': 28,
        'mars': 31,
        'avril': 30,
        'mai': 31,
        'juin': 30,
        'juillet': 31,
        'août': 31,
        'septembre': 30,
        'octobre': 31,
        'novembre': 30,
        'décembre': 31
    }

    # Check for leap year
    if month == 'février' and year % 4 == 0 and (year % 100 != 0
                                                 or year % 400 == 0):
        return 29
    else:
        return months_fr.get(month, 'inconnu')


# Create two new columns: month and year
data['mois'] = data['date'].dt.month.map(assign_month_name)
data['année'] = data['date'].dt.year
data['energie_kwh'] = data['puissance_w'] / 1000

# Group data by day, month, and year
data['date'] = data['date'].dt.date
data_days = data.groupby(['date', 'mois', 'année'])['energie_kwh'
                                                    ].sum().reset_index()
data_days = data_days.groupby(['mois', 'année']).count().reset_index()
data_days = data_days.rename(columns={'date': 'nb_jours_obs'})
del data_days['energie_kwh']
print(data_days)

# Group data by month and year
data_month = data.groupby(['mois', 'année'])['energie_kwh'].sum().reset_index()

mois_ordre = [
    'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
    'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
]

newDf = pd.DataFrame(columns=['mois', 'année', 'energie_kwh'])
year = data_month['année'][0]
for i in mois_ordre:
    if i not in data_month['mois'].values:
        newDf.loc[len(newDf)] = {'mois': i, 'année': year, 'energie_kwh': 0}
data_month = pd.concat([data_month, newDf]).reset_index(drop=True)
data_month = data_month.sort_values(by=['mois'], key=lambda x: x.map(
    {v: i for i, v in enumerate(mois_ordre)}))
data_month = data_month.reset_index(drop=True)
data_month['nb_jours'] = data_month.apply(lambda row: days_number(
    row['mois'], row['année']), axis=1)
data_month = pd.merge(data_month, data_days, on=['mois', 'année'], how='left')
data_month['complet'] = data_month['nb_jours'] == data_month['nb_jours_obs']
print(data_month)
data_month.to_csv('input/conso.csv',sep=',')

nrj_juin = data_month[data_month['mois'] == 'juin']['energie_kwh'].values
jrs_juin = data_month[data_month['mois'] == 'juin']['nb_jours']
print(nrj_juin, jrs_juin)
nrj_septembre = 2588.25
jrs_septembre = data_month[data_month['mois'] == 'septembre']['nb_jours']
nrj_ref = nrj_juin / jrs_juin * jrs_septembre
facteur = nrj_septembre / nrj_ref
data_test = data.loc[data['mois'] == 'juin']
data_test.loc[:, 'energie_kwh'] = data_test['energie_kwh'] * facteur
res = data_test.groupby('mois')['energie_kwh'].sum()
print(res)