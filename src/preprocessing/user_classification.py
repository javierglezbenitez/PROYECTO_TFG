import pandas as pd

def classify_users(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    municipios_canarios = [
        'Gran Canaria','Tenerife','La Palma','La Gomera','El Hierro','Lanzarote','Fuerteventura',
        'Adeje','Agüimes','Arucas','Mogán','Telde','Vegueta','Santa Cruz de Tenerife',
        'Las Palmas de Gran Canaria','Ingenio','La Laguna','Haría','Gáldar','Teguise','Tuineje'
    ]

    df['Tipo'] = 'Desconocido'

    df.loc[df['owner_location'].str.contains('España|Spain', case=False, na=False), 'Tipo'] = 'Peninsular'

    pattern_canarias = '|'.join(municipios_canarios)
    df.loc[df['owner_location'].str.contains(pattern_canarias, case=False, na=False), 'Tipo'] = 'Canario'

    cond_turista = (
        (df['Tipo'] == 'Peninsular') &
        (~df['owner_location'].str.contains(pattern_canarias, case=False, na=False))
    )
    df.loc[cond_turista, 'Tipo'] = 'Turista'

    return df