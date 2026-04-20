import requests
from src.LLM.src.config import API_BASE_URL

def tool_get_island_data(island: str):
    url = f"{API_BASE_URL}/islas/{island}"
    r = requests.get(url)

    if r.status_code != 200:
        return {"error": f"isla '{island}' no encontrada"}

    return r.json()