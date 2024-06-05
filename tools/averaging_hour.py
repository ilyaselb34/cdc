import pandas as pd


def averaging_low_step(data: pd.DataFrame):
    # Copy the data to avoid modifying the original DataFrame in case it needs
    # to be studied
    df = data.copy()
    df['date'] = df['date'].dt.floor('h')
    df['count'] = df.groupby('date')['date'].transform('count')
    df['type_valeur'] = df['count'].apply(
        lambda x: 'Mesurée' if x == 1 else 'à moyenner')
    df.drop(columns=['count'], inplace=True)

    averaged = df[df['type_valeur'] == 'à moyenner'].groupby('date')[
        'puissance_w'].mean().reset_index()
    averaged['type_valeur'] = 'Moyenne horaire'

    df = df[df['type_valeur'] == 'Mesurée']
    df = pd.concat([df, averaged], ignore_index=True)
    df = df.sort_values(by='date').reset_index(drop=True)

    return df
