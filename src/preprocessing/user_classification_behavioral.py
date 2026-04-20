import pandas as pd
from collections import Counter

def classify_users_behavioral(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "owner" not in df.columns:
        raise ValueError("El dataset no contiene la columna 'owner'.")

    if "datetaken" not in df.columns:
        df["datetaken"] = pd.NaT

    def get_island(row):
        lat = row["latitude"]
        lon = row["longitude"]
        if pd.isna(lat) or pd.isna(lon):
            return None

        if 27.5 <= lat <= 28.3 and -18.3 <= lon <= -17.9:
            return "El Hierro"
        if 27.7 <= lat <= 28.3 and -17.4 <= lon <= -17.0:
            return "La Gomera"
        if 28.4 <= lat <= 28.9 and -17.9 <= lon <= -17.6:
            return "La Palma"
        if 28.0 <= lat <= 28.3 and -16.9 <= lon <= -16.3:
            return "Tenerife"
        if 28.8 <= lat <= 29.3 and -13.9 <= lon <= -13.4:
            return "Lanzarote"
        if 28.0 <= lat <= 28.6 and -14.4 <= lon <= -13.6:
            return "Fuerteventura"
        if 27.9 <= lat <= 28.3 and -15.7 <= lon <= -15.3:
            return "Gran Canaria"

        return None

    df["isla"] = df.apply(get_island, axis=1)

    users = []

    for owner, subset in df.groupby("owner"):

        score_local = 0
        score_turista = 0

        islas = subset["isla"].dropna()
        if len(islas) > 0:
            conteo = Counter(islas)
            isla_principal, frecuencia = conteo.most_common(1)[0]
            proporción = frecuencia / len(islas)

            if proporción >= 0.75:
                score_local += 1
            if len(conteo) > 1:
                score_turista += 1

        fechas = subset["datetaken"].dropna()

        if len(fechas) > 0:
            meses = fechas.dt.to_period("M").nunique()
            dias = fechas.dt.date.nunique()

            if meses >= 4:
                score_local += 1

            if dias <= 10:
                score_turista += 1

        n_fotos = len(subset)
        if n_fotos <= 3:
            score_turista += 1

        if score_local == 0 and score_turista == 0:
            tipo = "Desconocido"
        elif score_local > score_turista:
            tipo = "Local"
        elif score_turista > score_local:
            tipo = "Turista"
        else:
            tipo = "Desconocido"

        users.append((owner, tipo))

    df_users = pd.DataFrame(users, columns=["owner", "Tipo_behavior"])

    df = df.merge(df_users, on="owner", how="left")

    return df