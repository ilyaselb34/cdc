"""
Author: Ilyas El Boujadaini

Content: Definition of the data correction functions.
"""
import pandas as pd
import linear_interpolation as itrp
import duplication as dpc


def dataset_correction(data: pd.DataFrame, wanted_step: int):
    """Correct the time step for irregular real data. Time step that are
    superior to 4 hours (240 minutes) are not corrected yet.

    Args:
        data (pd.DataFrame): pandas Dataframe with the data to correct,
            columns are 'date' and 'puissance_w'.
        wanted_step (int): the wanted time step between each data point
            (in minutes).

    Returns:
        res (pd.DataFrame): the corrected data.
    """

    res = pd.DataFrame(columns=['date', 'puissance_w', 'valeur_mesuree'])

    # Adds a column with the time step between each data point
    time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    data['time_step'] = [0] + time_step

    # At first, we use linear interpolation for low time steps
    res.loc[0] = [data['date'][0], data['puissance_w'][0],
                  data['valeur_mesuree'][0]]
    for i in range(1, len(data)):
        if data['time_step'][i] > wanted_step and data['time_step'][i] < 240:
            res = pd.concat([res,
                             itrp.linear_interpolation(data, i, wanted_step)],
                            ignore_index=True)
        else:
            res.loc[len(res)] = [data['date'][i], data['puissance_w'][i],
                                 data['valeur_mesuree'][i]]

    time_step = (res['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    res['time_step'] = [0] + time_step

    # Then we duplicate the data for time steps superior to 240 minutes
    res2 = pd.DataFrame(columns=['date', 'puissance_w', 'valeur_mesuree'])
    for j in range(1, len(res)):
        if res['time_step'][j] >= 240:
            res2 = pd.concat([res2, dpc.data_duplication(res, j, wanted_step)],
                             ignore_index=True)
    res = pd.concat([res, res2], ignore_index=True)
    res = res.sort_values(by='date').reset_index(drop=True)
    del res['time_step']
    del data['time_step']

    return res
