import json
import pandas as pd
from pathlib import Path

def load_json_to_df(json_path: str) -> pd.DataFrame:

    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {json_path}")

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    normalized = []
    for item in data:
        row = item.copy()

        loc = row.get("owner_location", "Desconocida")
        if isinstance(loc, dict):
            row["owner_location"] = loc.get("_content", "Desconocida")
        else:
            row["owner_location"] = loc

        try:
            row["latitude"] = float(row.get("latitude", 0))
            row["longitude"] = float(row.get("longitude", 0))
        except:
            row["latitude"] = None
            row["longitude"] = None

        try:
            row["views"] = int(row.get("views", 0))
        except:
            row["views"] = 0

        normalized.append(row)

    df = pd.DataFrame(normalized)

    df['datetaken'] = pd.to_datetime(df['datetaken'], errors='coerce')

    return df