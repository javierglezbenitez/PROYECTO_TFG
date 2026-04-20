from fastapi import FastAPI, HTTPException
import pandas as pd
import ast

CSV_PATH = r"C:\Users\cgsos\Documents\Cuarto\TFG\FLICKR\datos\LLM\Dataset\dataset_final_islas_canarias.csv"
df = pd.read_csv(CSV_PATH)

def fix_list(x):
    if pd.isna(x):
        return []
    try:
        return ast.literal_eval(x)
    except Exception:
        return []

df["alojamiento_list"] = df["alojamiento_list"].apply(fix_list)
df["restaurante_list"] = df["restaurante_list"].apply(fix_list)
df["playa_list"] = df["playa_list"].apply(fix_list)

api_data = {}

for isla, sub in df.groupby("isla"):
    api_data[isla] = {}

    for _, row in sub.iterrows():
        municipio = row["municipio"]

        api_data[isla][municipio] = {
            "nivel_turistico": int(row["nivel_turistico_municipio"]),
            "nivel_turistico_medio": float(row["nivel_turistico_medio"]),
            "n_clusters": int(row["n_clusters"]),
            "clusters_ids": row["clusters_ids"],

            "n_fotos_turistico": int(row.get("n_fotos_turistico", 0)),
            "n_fotos_local": int(row.get("n_fotos_local", 0)),

            "alojamientos": row["alojamiento_list"],
            "restaurantes": row["restaurante_list"],
            "playas": row["playa_list"]
        }

app = FastAPI(
    title="API Municipios Canarias",
    description="API neutra basada en niveles turísticos agregados desde clusters HDBSCAN",
    version="3.0"
)

@app.get("/")
def root():
    return {"status": "OK", "message": "API Municipios Canarias"}

@app.get("/all")
def get_all():
    return api_data

@app.get("/islas")
def get_islas():
    return list(api_data.keys())

@app.get("/islas/{isla}")
def get_isla(isla: str):
    isla = isla.title()
    if isla not in api_data:
        raise HTTPException(status_code=404, detail="Isla no encontrada")
    return api_data[isla]

@app.get("/islas/{isla}/{municipio}")
def get_municipio(isla: str, municipio: str):
    isla = isla.title()
    municipio = municipio.title()

    if isla not in api_data:
        raise HTTPException(status_code=404, detail="Isla no encontrada")

    if municipio not in api_data[isla]:
        raise HTTPException(
            status_code=404,
            detail=f"Municipio '{municipio}' no encontrado en {isla}"
        )

    return api_data[isla][municipio]

@app.get("/islas/{isla}/nivel/{nivel}")
def get_municipios_por_nivel(isla: str, nivel: int):
    isla = isla.title()

    if isla not in api_data:
        raise HTTPException(status_code=404, detail="Isla no encontrada")

    if nivel not in [1, 2, 3, 4]:
        raise HTTPException(
            status_code=400,
            detail="Nivel turístico inválido (1–4)"
        )

    return {
        m: info
        for m, info in api_data[isla].items()
        if info["nivel_turistico"] == nivel
    }


#http://127.0.0.1:8000/docs