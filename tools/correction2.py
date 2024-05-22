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
        df (pd.DataFrame): pandas DataFrame with the data to correct,
            columns are 'date', 'puissance_w', 'valeur_mesuree'.
        wanted_step (int): the wanted time step between each data point
            (in minutes).

    Returns:
        res (pd.dfFrame): the corrected data.
    """

    res = pd.DataFrame(columns=['date', 'puissance_w', 'valeur_mesuree'])
    pas_temps = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    data['pas_temps'] = [0] + pas_temps

    # Adds a column with the time step between each data point
    df = data.copy()
    df.loc[df['pas_temps'] < 60, 'date'] = df.loc[
        df['pas_temps'] < 60, 'date'].apply(lambda x: x.replace(minute=0))
    df = df.groupby('date')['puissance_w'].mean().reset_index()
    df['valeur_mesuree'] = 'Oui'
    df['pas_temps'] = [0] + (df['date'].diff() / pd.Timedelta(minutes=1)
                             ).fillna(0)
    # At first, we use linear interpolation for low time steps
    res.loc[0] = [df['date'][0], df['puissance_w'][0],
                  df['valeur_mesuree'][0]]
    for i in range(1, len(df)):
        if df['pas_temps'][i] > wanted_step and df['pas_temps'][i] < 240:
            res = pd.concat([res,
                             itrp.linear_interpolation(df, i, wanted_step)],
                            ignore_index=True)
        else:
            res.loc[len(res)] = [df['date'][i], df['puissance_w'][i],
                                 df['valeur_mesuree'][i]]

    pas_temps = (res['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    res['pas_temps'] = [0] + pas_temps

    # Then we duplicate the data for time steps superior to 240 minutes
    res2 = pd.DataFrame(columns=['date', 'puissance_w', 'valeur_mesuree'])
    for j in range(1, len(res)):
        if res['pas_temps'][j] >= 240:
            res2 = pd.concat([res2, dpc.data_duplication(res, j, wanted_step)],
                             ignore_index=True)
    res = pd.concat([res, res2], ignore_index=True)
    res = res.sort_values(by='date').reset_index(drop=True)
    del res['pas_temps']
    del data['pas_temps']

    return res
