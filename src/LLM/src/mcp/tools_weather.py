import requests

coords = {
    "Gran Canaria": (28.1, -15.4),
    "Tenerife": (28.3, -16.6),
    "Fuerteventura": (28.4, -14.0),
    "Lanzarote": (29.0, -13.6),
    "La Palma": (28.6, -17.8),
    "La Gomera": (28.1, -17.1),
    "El Hierro": (27.7, -18.0)
}

WEATHER_CODES = {
    0: "Despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Neblina",
    48: "Neblina con escarcha",
    51: "Llovizna ligera",
    53: "Llovizna moderada",
    55: "Llovizna intensa",
    61: "Lluvia ligera",
    63: "Lluvia moderada",
    65: "Lluvia intensa",
    71: "Nieve ligera",
    73: "Nieve moderada",
    75: "Nieve intensa"
}

def tool_get_weather(island: str):

    if island not in coords:
        return {"error": "Isla no reconocida."}

    lat, lon = coords[island]

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )

    r = requests.get(url)
    if r.status_code != 200:
        return {"error": "No se pudo obtener el clima"}

    data = r.json()
    cw = data.get("current_weather", {})

    code = cw.get("weathercode")
    visual = WEATHER_CODES.get(code, "Condición desconocida")

    return {
        "temperature": cw.get("temperature"),
        "windspeed": cw.get("windspeed"),
        "visual": visual
    }