"""
Author: Ilyas El Boujadaini

Content: Definition of the data correction function.
"""

import pandas as pd
import linear_interpolation as itrp
import duplication as dpc
import averaging_hour as avg


def dataset_correction(data: pd.DataFrame, wanted_step: int):
    """Correct the time step for irregular real data. Time step that are
    superior to 4 hours (240 minutes) are not corrected yet.

    Args:
        df (pd.DataFrame): pandas DataFrame with the data to correct,
            columns are 'date', 'puissance_w', 'type_valeur'.
        wanted_step (int): the wanted time step between each data point
            (in minutes).

    Returns:
        res (pd.dfFrame): the corrected data.
    """

    res = pd.DataFrame(columns=['date', 'puissance_w', 'type_valeur'])
    data['pas_temps'] = [0] + (data['date'].diff() / pd.Timedelta(minutes=1)
                               ).fillna(0)

    # Cette fonction permet de moyenner les données à pas de temps faible
    # (<60min)
    df = avg.averaging_low_step(data)

    for i in range(1, len(df)):
        # On utiliste l'interpolation linéaire pour les pas de temps inférieurs
        # à 240 minutes (4 heures)
        if df['pas_temps'][i] > wanted_step and df['pas_temps'][i] < 240:
            res = pd.concat([res, itrp.linear_interpolation(df, i, wanted_step)
                             ],
                            ignore_index=True)
        else:
            res.loc[len(res)] = [df['date'][i], df['puissance_w'][i],
                                 df['type_valeur'][i]]

    res['pas_temps'] = [0] + (res['date'].diff() / pd.Timedelta(minutes=1)
                              ).fillna(0)

    # On utilise la duplication de données par moyenne mobile pour les pas de
    # temps supérieurs à 240 minutes
    res2 = pd.DataFrame(columns=['date', 'puissance_w', 'type_valeur'])
    for j in range(1, len(res)):
        if res['pas_temps'][j] >= 240:
            dup = dpc.data_duplication2(res, j, wanted_step)
            if not dup.empty and not dup.isna().all().all():
                res2 = pd.concat([res2, dup], ignore_index=True)
            else:
                print("Skipping empty or all-NA DataFrame")
    if not res2.empty and not res2.isna().all().all():
        res = pd.concat([res, res2], ignore_index=True)
        res = res.sort_values(by='date').reset_index(drop=True)
        del res['pas_temps']
        del data['pas_temps']

    return res
