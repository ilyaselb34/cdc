"""
Author: Ilyas El Boujadaini

Content: Definition of the data duplication related functions.

"""
import pandas as pd
import datetime as dt


def duplicable(data: pd.DataFrame, time: dt.datetime, wanted_step: int):
    """Verify if a date is duplicable by checking if a similar date exists in
    the dataset.

    Args:
        data (pd.DataFrame): Dataframe with the raw data to check, columns are
            'date', 'puissance_w' and 'valeur_mesuree'.
        time (dt.datetime): the date to verify in dt.datetime format.
        wanted_step (int): the time step required between each data point.

    Returns:
        res: boolean, True if the date is duplicable, False otherwise.
    """
    res = True

    # This column is created to study the time step between each data point
    time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
    data['time_step'] = [0] + time_step
    i = data[data['date'] == time].index[0]
    cumul_step = 0

    if data['date'].isin([time]).any():
        # Iterate over the data points before the studied date
        # to check if the time step is regular
        while (i >= 0 and cumul_step < wanted_step and res):
            if data['time_step'][i] > wanted_step:
                res = False
            else:
                cumul_step += data['time_step'][i]
                i -= 1
            if i == 0:
                res = False
    else:
        res = False
    return res


def data_duplication(data: pd.DataFrame, ind_step: int, wanted_step: int):
    """Duplicate the data if the time step is too big.

    Args:
        data (pd.DataFrame): Dataframe with the raw data to check, columns are
            'date', 'puissance_w' and 'valeur_mesuree'.
        ind_step (int): the index of the irregular step to check.

    Returns:
        res (pd.DataFrame): the duplicated data.
    """

    res = pd.DataFrame(columns=['date', 'puissance_w', 'valeur_mesuree'])

    date_found = False
    i = 1

    # Iterate in a 3-week range to find a substitution date
    while (i <= 3 and not date_found):
        cond_1 = data['date'].isin([data['date'][ind_step]
                                    + dt.timedelta(days=i * 7)]).any()
        cond_2 = data['date'].isin([data['date'][ind_step]
                                    - dt.timedelta(days=i * 7)]).any()

        if (cond_1 or cond_2):
            sub_date1 = data['date'][ind_step] + dt.timedelta(days=i * 7)
            sub_date2 = data['date'][ind_step] - dt.timedelta(days=i * 7)

            # Check if one of the substitution dates is duplicable
            if duplicable(data, sub_date1, wanted_step):
                date_found = True
                weeks = -i
                sub_date = sub_date1
            elif duplicable(data, sub_date2, wanted_step):
                date_found = True
                weeks = i
                sub_date = sub_date2
        i += 1

    if date_found:
        time_step = (data['date'].diff() / pd.Timedelta(minutes=1)).fillna(0)
        data['time_step'] = [0] + time_step
        j = data[data['date'] == sub_date].index[0] - 1
        cumul_step = 0
        # Iterate over the data points before the substitution date
        while (j > 0 and cumul_step < data['time_step'][ind_step]
               - wanted_step and date_found):
            if data['time_step'][j] > wanted_step:
                date_found = False
            else:
                # Add the data points to the new dataframe
                res.loc[len(res)] = [data['date'][j], data['puissance_w'][j],
                                     'Non']
                cumul_step += data['time_step'][j]
                j -= 1
        # Correct the new data points by adding or removing the number of weeks
        res['date'] = res['date'] + dt.timedelta(days=7 * weeks)
    else:
        print('No substitution date found.')
        res = pd.DataFrame(columns=['date', 'puissance_w', 'valeur_mesuree'])
    return res

def data_duplication2(data: pd.DataFrame, ind_step: int, wanted_step: int):
    """_summary_

    Args:
        data (pd.DataFrame): _description_
        ind_step (int): _description_
        wanted_step (int): _description_
    """

    res = pd.DataFrame(columns=['date', 'puissance_w', 'valeur_mesuree'])
    i = 1
    