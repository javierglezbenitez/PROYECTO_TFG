ISLAND_ALIASES = {
    "tenerife": "Tenerife",
    "teneriffa": "Tenerife",
    "tf": "Tenerife",
    "tfe": "Tenerife",
    "Tenerife" : "Tenerife",

    "gran canaria": "Gran Canaria",
    "granca": "Gran Canaria",
    "gc": "Gran Canaria",
    "Gran Canaria": "Gran Canaria",

    "lanzarote": "Lanzarote",
    "lanza": "Lanzarote",
    "lanzarota": "Lanzarote",
    "Lanzarote" : "Lanzarote",

    "fuerteventura": "Fuerteventura",
    "ftv": "Fuerteventura",
    "Fuerteventura" : "Fuerteventura",

    "la palma": "La Palma",
    "La Palma" : "La Palma",
    "la Palma" : "La Palma",

    "la gomera": "La Gomera",
    "gomera": "La Gomera",
    "La Gomera" : "La Gomera",
    "la Gomera" : "La Gomera",

    "el hierro": "El Hierro",
    "hierro": "El Hierro",
    "El Hierro" : "El Hierro",
    "el Hierro" : "El Hierro"
}

def normalize_island(text: str):
    msg = text.lower().strip()
    for alias, canonical in ISLAND_ALIASES.items():
        if alias in msg:
            return canonical
    return None

def normalize_municipio(text: str):
    if not text:
        return None
    return text.strip().title()

INTENT_KEYWORDS = [
    "recomiéndame", "recomiendame",
    "recomienda",
    "quiero visitar",
    "que visitar",
    "planeo ir",
    "planes",
    "sitios",
    "playas",
    "donde ir",
    "dónde ir",
    "qué ver",
    "que ver",
    "me recomiendas",
    "qué me sugieres",
    "que me sugieres"
]
def user_wants_recommendation(text: str):
    msg = text.lower()
    return any(k in msg for k in INTENT_KEYWORDS)