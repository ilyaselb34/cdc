import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import datetime as dt


def assign_month_name(month_num: int):
    """This function assigns the month name in French based on the month
       number.

    Args:
        month_num (int): the month number from 1 to 12

    Returns:
        res (str): string representing the month in French
    """
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
    res = months_fr.get(month_num, 'inconnu')
    return res


def get_season_color(date: dt.datetime):
    """Attributes a color to a date based on the season.

    Args:
        date (dt.datetime): the date to attribute a color to

    Returns:
        res (str): the name of the season corresponding to the date
    """
    year = date.year
    spring = pd.Timestamp(f'{year}-03-21')
    summer = pd.Timestamp(f'{year}-06-21')
    autumn = pd.Timestamp(f'{year}-09-21')
    winter = pd.Timestamp(f'{year}-12-21')

    if spring <= date < summer:
        res = 'green'  # Spring
    elif summer <= date < autumn:
        res = 'yellow'  # Summer
    elif autumn <= date < winter:
        res = 'orange'  # Autumn
    else:
        res = 'blue'  # Winter
    return res


# Load data
def boxplot_profil_journalier(data: pd.DataFrame, prefix: str,
                              date_min: dt.datetime, date_max: dt.datetime,
                              outfile: str):
    """This function creates a boxplot of the daily consumption for each day
       of the week.

    Args:
        data (pd.Dataframe): the cleaned data to plot
        prefix (str): the name of the studied CSV file, without the extension
        date_min (dt.datetime): the starting date of the data
        date_max (dt.datetime): the ending date of the data
        outfile (str): the output directory
    Returns:
        None
    """
    exit_path = os.path.join(outfile, prefix + '_boxplot_journalier.png')
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

    # Apply the function to the 'date' column to create the 'couleur' column
    data_week['couleur'] = data_week['date'].apply(get_season_color)

    del data_week['date_sans_heure']
    del data_week['puissance_w']
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='jour_semaine', y='energie_kwh', data=data_week,
                showfliers=False, order=['lundi', 'mardi', 'mercredi', 'jeudi',
                                         'vendredi', 'samedi', 'dimanche'],
                color='white')

    for color in data_week['couleur'].unique():
        sns.stripplot(x='jour_semaine', y='energie_kwh',
                        data=data_week[data_week['couleur'] == color],
                        color=color, alpha=0.5, jitter=True,
                        order=['lundi', 'mardi', 'mercredi', 'jeudi',
                               'vendredi', 'samedi', 'dimanche'])

    sns.pointplot(x='jour_semaine', y='energie_kwh', data=data_week,
                    order=['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi',
                           'samedi', 'dimanche'], estimator=np.mean,
                    errorbar=None, color='red', markers='D', linestyles='',
                    label='Moyenne')

    handles, labels = plt.gca().get_legend_handles_labels()
    handles.append(plt.Line2D([0], [0], marker='o', color='w',
                              label='Données Individuelles',
                              markerfacecolor='black', markersize=10))
    plt.legend(handles=handles)
    plt.xlabel('Jour de la semaine')
    plt.ylabel('Consommation Journalière (kWh)')
    plt.title(f'Consommation par jour de la semaine\n'
              f'Ce graphique concerne des valeurs récoltées du {date_min} au'
              f' {date_max}')
    plt.ylim(bottom=0)
    plt.savefig(exit_path)


def barplot_profil_annuel(data: pd.DataFrame, prefix: str,
                          date_min: dt.datetime, date_max: dt.datetime,
                          outfile: str):
    """This function creates a barplot of the monthly consumption for each
       month

    Args:
        data (pd.Dataframe): the cleaned data to plot
        prefix (str): the name of the studied CSV file, without the extension
        date_min (dt.datetime): the starting date of the data
        date_max (dt.datetime): the ending date of the data
        outfile (str): the output directory
    Returns:
        None
    """
    data['mois'] = data['date'].dt.month
    data['nom_mois'] = data['mois'].map(assign_month_name)
    data['année'] = data['date'].dt.year

    grouped_data = data.groupby(['année', 'mois', 'nom_mois'])
    data_month = grouped_data['puissance_w'].sum().reset_index()

    data_month['energie_kwh'] = data_month['puissance_w'] / 1000
    del data_month['puissance_w']

    for i in range(1, 13):
        if i not in data_month['mois'].values:
            ligne = pd.DataFrame(
                {'mois': i, 'nom_mois': assign_month_name(i),
                 'année': data_month['année'][0],
                 'energie_kwh': 0},
                index=[0])
            data_month = pd.concat([data_month, ligne]).reset_index(drop=True)
    data_month = data_month.sort_values(by=['mois']).reset_index(drop=True)
    print(data_month)
    print(data_month.dtypes)

    data_month['couleur'] = 'blue'
    data_month.loc[(data_month['mois'] >= 4) & (data_month['mois'] <= 6),
                   'couleur'] = 'green'
    data_month.loc[(data_month['mois'] >= 7) & (data_month['mois'] <= 9),
                   'couleur'] = 'yellow'
    data_month.loc[data_month['mois'] >= 10, 'couleur'] = 'orange'

    exit_path = os.path.join(outfile, prefix + '_profil_annuel.png')

    plt.figure(figsize=(12, 6))
    sns.barplot(x='nom_mois', y='energie_kwh', data=data_month,
                palette=data_month['couleur'].tolist())
    plt.xlabel('Mois')
    plt.ylabel('Energie (kWh)')
    plt.title(f'Consommation par mois\nCe graphique concerne des valeurs'
              f'récoltées du {date_min} au {date_max}')

    handles = [
        mpatches.Patch(color='green', label='Printemps'),
        mpatches.Patch(color='yellow', label='Été'),
        mpatches.Patch(color='orange', label='Automne'),
        mpatches.Patch(color='blue', label='Hiver')
    ]
    plt.legend(handles=handles, title='Saison')
    plt.savefig(exit_path)


def lineplot_profil_horaire(data: pd.DataFrame, prefix: str,
                            date_min: dt.datetime, date_max: dt.datetime,
                            outfile: str):
    """This function creates a lineplot of the average power consumption for
       each hour of the day and for each day of the week.

    Args:
        data (pd.Dataframe): the cleaned data to plot
        prefix (str): the name of the studied CSV file, without the extension
        date_min (dt.datetime): the starting date of the data
        date_max (dt.datetime): the ending date of the data
        outfile (str): the output directory
    Returns:
        None
    """
    data['jour_semaine'] = data['date'].dt.strftime('%A')
    data['heure'] = data['date'].dt.strftime('%H:%M:%S')

    weekly_data = data.groupby(['jour_semaine', 'heure'])[
        'puissance_kw'].mean().reset_index()
    mean_data = weekly_data.groupby('heure')['puissance_kw'
                                             ].mean().reset_index()

    exit_path = os.path.join(outfile, prefix + '_profil_horaire.png')

    plt.figure(figsize=(12, 8))
    ax = plt.subplot(111)

    colors = ['red', 'orange', 'yellow', 'pink', 'purple', 'cyan', 'blue']

    for i, day in enumerate(['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi',
                            'samedi', 'dimanche']):
        day_data = weekly_data[weekly_data['jour_semaine'] == day]
        ax.plot(day_data['heure'], day_data['puissance_kw'],
                linestyle='-', color=colors[i], label=day)

    ax.plot(mean_data['heure'], mean_data['puissance_kw'], color='black',
            linestyle='-', linewidth=4, label='Moyenne Générale')

    plt.xlabel('Heure')
    plt.ylabel('Puissance Moyenne (kW)')
    plt.title(f'Profil de la Puissance Moyenne par Heure pour Chaque Jour de '
              'la Semaine\n'
              f'Ce graphique concerne des valeurs récoltées du {date_min} au '
              f'{date_max}')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.ylim(bottom=0)
    if mean_data['puissance_kw'].max() < 10:
        plt.ylim(top=10)
    plt.savefig(exit_path)
