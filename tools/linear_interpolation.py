"""
Author: Ilyas El Boujadaini

Content: Definition of the linear interpolation functions for
    irregular time steps.
"""

import pandas as pd
import datetime as dt


def linear_interpolation(data: pd.DataFrame, ind_step: int, wanted_step: int):
    """Cette fonction complète les données manquantes entre deux points de
    mesure consécutifs par interpolation linéaire

    Args:
        data (pd.DataFrame): le dataframe contenant les données à interpoler
        ind_step (int): l'indice du point de mesure à interpoler
        wanted_step (int): _description_

    Returns:
        _type_: _description_
    """
    # Create a new dataframe to store the interpolated data
    res = pd.DataFrame(columns=['date', 'puissance_w', 'type_valeur'])

    # Calculate the time step between this data point and the previous one
    # and then calculate the power scale to apply to the data points that
    # will be interpolated
    pas_temps = (data['date'][ind_step]
                 - data['date'][ind_step - 1]).total_seconds() / 60
    x = pas_temps // wanted_step
    pow_scale = (data['puissance_w'][ind_step]
                 - data['puissance_w'][ind_step - 1]) / (int(x))

    # Interpolate the time step  and the power between the two data points
    for i in range(1, int(x)):
        res.loc[len(res)] = [data['date'][ind_step - 1]
                             + dt.timedelta(minutes=(wanted_step * i)),
                             data['puissance_w'][ind_step - 1]
                             + pow_scale * (i), 'Interpolée']
    res.loc[len(res)] = [data['date'][ind_step], data['puissance_w'][ind_step],
                         data['type_valeur'][ind_step]]

    return res


def dataset_linear_interpolation(data: pd.DataFrame, wanted_step: int):
    """Interpolate the time step for irregular real data.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to interpolate,
            columns are 'date' and 'puissance_w'.
        wanted_step (int): the wanted time step between two consecutive
            data points (in minutes).

    Returns:
        res (pd.DataFrame): the corrected data.
    """

    res = pd.DataFrame(columns=['date', 'puissance_w', 'type_valeur'])

    # Add a new column to the dataframe with the time step between
    # two consecutive data points
    data['pas_temps'] = [0] + (data['date'].diff() / pd.Timedelta(minutes=1)
                               ).fillna(0)

    # Interpolate the data points with a time step bigger
    # than the wanted time step
    res.loc[0] = [data['date'][0], data['puissance_w'][0],
                  data['type_valeur'][0]]
    for i in range(1, len(data)):
        if data['pas_temps'][i] > wanted_step:
            res = pd.concat([res, linear_interpolation(data, i, wanted_step)],
                            ignore_index=True)
        else:
            res.loc[len(res)] = [data['date'][i], data['puissance_w'][i],
                                 data['type_valeur'][i]]

    del data['pas_temps']

    return res
