from pathlib import Path
import json
import pandas as pd

from src.preprocessing.cleaning import clean_dataframe
from src.preprocessing.export import export_clean_df
from src.preprocessing.user_classification_advanced import classify_users_advanced

RAW_DIR = Path("/Users/cgsos/Documents/Cuarto/TFG/FLICKR/datos/raw/fotos_canarias")
OUTPUT = "/Users/cgsos/Documents/Cuarto/TFG/FLICKR/datos/processed/fotos_canarias.csv"


def normalize_owner_location_column(df):
    if "owner_location" not in df.columns:
        df["owner_location"] = "Desconocida"

    def normalize(val):
        if isinstance(val, dict):
            return val.get("_content", "Desconocida")
        if val is None:
            return "Desconocida"
        return str(val)

    df["owner_location"] = df["owner_location"].apply(normalize)
    return df


def run_pipeline():
    json_files = list(RAW_DIR.glob("*.json"))

    if not json_files:
        raise RuntimeError(
            "ERROR: No hay JSON en datos/raw/canarias/. "
            "Ejecuta primero download_all_canarias.py"
        )

    print(f" Encontrados {len(json_files)} archivos descargados de islas.\n")

    all_items = []

    for file in json_files:
        island_name = file.stem.replace("_", " ").title()

        with open(file, "r", encoding="utf-8") as f:
            items = json.load(f)

        for item in items:
            item["isla"] = island_name

        all_items.extend(items)

    print(f"\n Total registros brutos combinados: {len(all_items)}")

    df = pd.DataFrame(all_items)

    df = normalize_owner_location_column(df)

    numeric_cols = ["latitude", "longitude", "views"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "datetaken" in df.columns:
        df["datetaken"] = pd.to_datetime(df["datetaken"], errors="coerce")
    else:
        df["datetaken"] = pd.NaT

    df = clean_dataframe(df)

    df = classify_users_advanced(df)

    export_clean_df(df, OUTPUT)

    print("\n Dataset final construido correctamente")
    print(f" Guardado en: {OUTPUT}")
    print(f" Total registros finales: {len(df)}\n")

if __name__ == "__main__":
    run_pipeline()