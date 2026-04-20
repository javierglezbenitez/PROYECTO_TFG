import pandas as pd
import numpy as np
from geopy.distance import geodesic

def compute_user_features(df: pd.DataFrame):

    user_features = []

    for owner, sub in df.groupby("owner"):

        sub = sub.dropna(subset=["latitude", "longitude"])

        n_fotos = len(sub)

        fechas = sub["datetaken"].dropna()
        n_dias = fechas.dt.date.nunique()
        n_meses = fechas.dt.to_period("M").nunique()

        n_islas = sub["isla"].nunique()
        if n_islas > 0:
            isla_principal_prop = sub["isla"].value_counts(normalize=True).iloc[0]
        else:
            isla_principal_prop = 0

        fotos_por_dia = n_fotos / max(n_dias, 1)

        coords = list(zip(sub["latitude"], sub["longitude"]))
        distancias = []
        for i in range(1, len(coords)):
            try:
                distancias.append(geodesic(coords[i-1], coords[i]).km)
            except:
                pass

        distancia_media = np.mean(distancias) if distancias else 0
        distancia_max = np.max(distancias) if distancias else 0

        views_median = sub["views"].median()

        user_features.append({
            "owner": owner,
            "n_fotos": n_fotos,
            "n_dias": n_dias,
            "n_meses": n_meses,
            "n_islas": n_islas,
            "isla_principal_prop": isla_principal_prop,
            "fotos_por_dia": fotos_por_dia,
            "distancia_media": distancia_media,
            "distancia_max": distancia_max,
            "views_median": views_median,
        })

    return pd.DataFrame(user_features)

def classify_user_row(f):
    score_local = 0
    score_turista = 0

    if f["n_dias"] <= 15:
        score_turista += 2
    if f["n_meses"] <= 2:
        score_turista += 1

    if f["n_fotos"] >= 40:
        score_local += 2
    if f["n_fotos"] <= 3:
        score_turista += 2

    if f["n_islas"] == 1 and f["isla_principal_prop"] >= 0.75:
        score_local += 2
    if f["n_islas"] >= 3:
        score_turista += 3

    if f["distancia_media"] > 20:
        score_turista += 2
    if f["distancia_media"] < 5:
        score_local += 1

    if f["distancia_max"] > 80:
        score_turista += 2

    if f["views_median"] > 1500:
        score_turista += 1

    if score_local - score_turista >= 2:
        return "Local"
    elif score_turista - score_local >= 2:
        return "Turista"
    else:
        return "Desconocido"

def classify_users_advanced(df: pd.DataFrame) -> pd.DataFrame:

    feats = compute_user_features(df)

    feats["Tipo_behavior"] = feats.apply(classify_user_row, axis=1)

    df = df.merge(feats[["owner", "Tipo_behavior"]], on="owner", how="left")

    return df