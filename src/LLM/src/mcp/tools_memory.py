from src.LLM.src.db.db_manager import save_full_intent, get_user_profile, create_empty_user

async def tool_save_user_attribute(user_id: str, attribute: str, value, nombre=None):
    profile = get_user_profile(user_id, nombre=nombre)
    tipo = profile.get("tipo")

    intent_fake = {
        "is_local": tipo == "local",
        "is_tourist": tipo == "turista",
        "nombre": value if attribute == "nombre" else nombre,
    }

    if attribute in ["isla_residencia", "isla_destino", "island"]:
        intent_fake["island"] = value

    if attribute in ["municipio_residencia", "municipio"]:
        intent_fake["municipio"] = value

    if attribute == "lugar_origen" or attribute == "origin_city":
        intent_fake["origin_city"] = value

    if attribute == "ambiente":
        intent_fake["ambiente"] = value

    if attribute == "nivel_intencion":
        intent_fake["nivel_intencion"] = value

    if attribute == "municipio_recomendado":
        intent_fake["municipio_recomendado"] = value
    if attribute == "alternativa_1":
        intent_fake["alternativa_1"] = value
    if attribute == "alternativa_2":
        intent_fake["alternativa_2"] = value
    if attribute == "fecha_consulta":
        intent_fake["fecha_consulta"] = value
    if attribute == "tiempo_respuesta_ms":
        intent_fake["tiempo_respuesta_ms"] = value

    active_nombre = intent_fake["nombre"]
    if attribute == "nombre" and not tipo:
        create_empty_user(user_id, "turista", nombre=value)

    save_full_intent(user_id, active_nombre, intent_fake)

    return {
        "status": "saved",
        "attribute": attribute,
        "value": value,
        "profile_active": active_nombre
    }