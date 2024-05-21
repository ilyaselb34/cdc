"""
Author: Ilyas El Boujadaini

Content: Definition of the linear interpolation function for
irregular time steps.
"""

import pandas as pd
import datetime as dt


def linear_interpolation(data: pd.DataFrame, ind_step: int, wanted_step: int):
    """Data linear interpolation for irregular time step. Also interpolates
    whole days if the time step is too big, so we have to improve this
    functionnality later.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to interpolate,
            columns are 'date' and 'puissance_w'.
        ind_step (int): the index of the irregular step to correct.
        wanted_step (int): the wanted time step between each data point
            (in minutes).

    Returns:
        res (pd.DataFrame): the interpolated data.
    """

    # Creating a new dataframe to store the interpolated data
    res = pd.DataFrame(columns=['date', 'puissance_w', 'valeur_mesuree'])

    """Adds data points to the new dataframe, adapting the power value
    to the time step"""
    time_step = (data['date'][ind_step]
                 - data['date'][ind_step-1]).total_seconds() / 60
    x = time_step//wanted_step
    pow_scale = (data['puissance_w'][ind_step]
                 - data['puissance_w'][ind_step-1])/(int(x))
    for i in range(1, int(x)):
        res.loc[len(res)] = [data['date'][ind_step-1]
                             + dt.timedelta(minutes=(wanted_step*i)),
                             data['puissance_w'][ind_step-1]+pow_scale*(i),
                             'Non']
    res.loc[len(res)] = [data['date'][ind_step], data['puissance_w'][ind_step],
                         data['valeur_mesuree'][ind_step]]

    return res


def dataset_linear_interpolation(data: pd.DataFrame, wanted_step: int):
    """Interpolate the time step for irregular real data.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to interpolate,
            columns are 'date' and 'puissance_w'.
        wanted_step (int): the wanted time step between each data point
            (in minutes).

    Returns:
        res (pd.DataFrame): the corrected data.
    """

    res = pd.DataFrame(columns=['date', 'puissance_w', 'valeur_mesuree'])

    """Adds a new column to the dataframe with the time step between each data
    point"""
    time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    data['time_step'] = [0]+time_step

    """Interpolates the data points with a time step bigger than the wanted
    time step"""
    res.loc[0] = [data['date'][0], data['puissance_w'][0],
                  data['valeur_mesuree'][0]]
    for i in range(1, len(data)):
        if data['time_step'][i] > wanted_step:
            res = pd.concat([res, linear_interpolation(data, i, wanted_step)],
                            ignore_index=True)
        else:
            res.loc[len(res)] = [data['date'][i], data['puissance_w'][i],
                                 data['valeur_mesuree'][i]]

    del data['time_step']

    return res
