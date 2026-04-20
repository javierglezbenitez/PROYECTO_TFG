import re
from src.LLM.src.mcp.tools_normalizer import normalize_island, normalize_municipio

def classify_ambiente(text: str) -> str:

    text = text.lower()

    keywords_autentico = [
        "como turista", "como un turista", "sentirme turista",
        "como canario", "como un canario", "canario más",
        "como local", "sentirme como un local",
        "vivir la isla", "desde dentro", "experiencia auténtica"
    ]

    if any(k in text for k in keywords_autentico):
        return "autentico"

    if any(w in text for w in [
        "relax total", "ambiente relax", "plan relax",
        "desconectar del todo", "descanso", "relajarse"
    ]):
        return "relax"

    if any(w in text for w in [
        "ambiente confort",
        "plan confort",
        "viaje de confort",
        "lujo", "lujoso",
        "alta gama",
        "todo incluido",
        "hotel de lujo",
        "experiencia premium"
    ]):
        return "confort"

    if any(w in text for w in ["fiesta", "animado", "ocio", "diversión"]):
        return "animado"

    return "estandar"


def classify_intent(message: str):

    msg = message.lower().strip()

    intent = {
        "is_local": False,
        "is_tourist": False,

        "nombre": None,
        "origin_city": None,

        "island": None,
        "municipio": None,

        "ambiente": "estandar",

        "signals": {
            "muy_local": False,
            "flexible": False,
            "turistico": False,
            "evita_masas": False,
            "cambio_rol": False
        },

        "request_recommendation": False
    }

    if any(w in msg for w in [
        "soy local", "residente", "vivo en", "resido en", "soy de aquí"
    ]):
        intent["is_local"] = True

    if any(w in msg for w in [
        "soy turista", "estoy de viaje", "vacaciones", "turismo"
    ]):
        intent["is_tourist"] = True

    if intent["is_local"]:
        match_muni = re.search(
            r"(?:vivo en|resido en|soy de)\s+([a-záéíóúñ\s]+)",
            msg
        )
        if match_muni:
            municipio_raw = match_muni.group(1).strip().title()
            intent["municipio"] = normalize_municipio(municipio_raw)

    if not intent["is_local"]:
        match_origen = re.search(
            r"(?:vengo de|procedo de|soy de)\s+([a-záéíóúñ\s]+)",
            msg
        )
        if match_origen:
            ciudad = match_origen.group(1).strip().title()
            if not normalize_island(ciudad.lower()):
                intent["origin_city"] = ciudad
                intent["is_tourist"] = True

    match_nombre = re.search(
        r"(?:me llamo|mi nombre es)\s+([a-záéíóúñ]+)",
        msg
    )
    if match_nombre:
        intent["nombre"] = match_nombre.group(1).title()

    intent["island"] = normalize_island(msg)
    if intent["island"]:
        intent["request_recommendation"] = True

    intent["ambiente"] = classify_ambiente(msg)
    if intent["ambiente"] == "autentico":
        intent["signals"]["cambio_rol"] = True


    if any(w in msg for w in [
        "muy local", "poco turístico", "de toda la vida",
        "tradicional", "vida cotidiana"
    ]):
        intent["signals"]["muy_local"] = True

    if any(w in msg for w in [
        "no masificado", "no masificados",
        "no estar masificado", "no estén masificados",
        "sin masificar", "sin aglomeraciones",
        "evitar masificación", "evitar turistas",
        "poco masificado"
    ]):
        intent["signals"]["evita_masas"] = True

    if any(w in msg for w in [
        "mezcla", "equilibrado", "me da igual",
        "ver otros sitios", "planes distintos",
        "ni muy turístico ni muy local"
    ]):
        intent["signals"]["flexible"] = True

    if any(w in msg for w in [
        "zonas turísticas", "ambiente turístico",
        "hoteles", "servicios", "sitios turísticos"
    ]):
        intent["signals"]["turistico"] = True

    return intent