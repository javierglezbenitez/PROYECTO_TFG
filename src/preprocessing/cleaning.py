import pandas as pd

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df.drop_duplicates(subset=["id"], inplace=True)

    df = df[(df['latitude'].notnull()) & (df['longitude'].notnull())]

    df['owner_location'] = df['owner_location'].fillna("Desconocida")
    df.loc[df['owner_location'] == "", 'owner_location'] = "Desconocida"

    df = df.sort_values(by='datetaken', ascending=True)

    return df