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


def assign_month_name(month_num):
    """Assigner les noms des mois en français à partir du numéro du mois.
       On n'utilise pas les fonctions de datetime pour éviter les problèmes
       d'encodage.

    Args:
        month_num (int): le numéro du mois

    Returns:
        res: mois en français ou 'inconnu' si le numéro du mois n'est pas
             dans le dictionnaire
    """

    # Dictionnaire des mois en français
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
    # Retourner le nom du mois ou 'inconnu' si le numéro du mois n'est pas
    # dans le dictionnaire
    res = months_fr.get(month_num, 'inconnu')
    return res


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

    # Vérifier si l'année est bissextile
    if month == 'février' and year % 4 == 0:
        res = 29
    else:
        # Retourner le nombre de jours du mois ou 'inconnu' si le mois n'est
        # pas dans le dictionnaire
        res = months_fr.get(month, 'inconnu')

    return res


# Appliquer la fonction pour créer une colonne 'mois'
data['mois'] = data['date'].dt.month.map(assign_month_name)

# Print unique months
print(data['mois'].unique())
