import pandas as pd
import locale

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

file_name = 'output/Enedis_SGE_HDM_A06GKIR0_cleaned.csv'
data = pd.read_csv(file_name, sep=',')
data['date'] = pd.to_datetime(data['date'])
data['puissance_w'] /= 1000
data = data.groupby(data['date'].dt.date, 'jour_semaine')['puissance_w'].sum().reset_index()
"data['jour_semaine'] = data['date'].dt.strftime('%A')"

print(data)