def tool_recommend_places(
    user_profile,
    island_data,
    user_id,
    island=None,
    ambiente="estandar",
    current_intent_muni=None
):
    tipo = user_profile.get("tipo")
    data = user_profile.get("data", {})

    muni_db = data.get("municipio")
    municipio_residencia = current_intent_muni or muni_db

    residencia_clean = (
        municipio_residencia.lower().strip()
        if municipio_residencia else None
    )

    nivel_objetivo = data.get("nivel_intencion")

    if nivel_objetivo is None:
        nivel_objetivo = 4 if tipo == "turista" else 2

    if ambiente == "autentico":
        if nivel_objetivo == 1:
            niveles_busqueda = [1, 2, 3]
        elif nivel_objetivo == 4:
            niveles_busqueda = [4, 3]
        else:
            niveles_busqueda = [nivel_objetivo]
    else:
        if nivel_objetivo == 1:
            niveles_busqueda = [1, 2, 3]
        elif nivel_objetivo == 2:
            niveles_busqueda = [2, 1, 3]
        elif nivel_objetivo == 3:
            niveles_busqueda = [3, 4]
        elif nivel_objetivo == 4:
            niveles_busqueda = [4, 3]
        else:
            niveles_busqueda = [nivel_objetivo]

    if ambiente == "autentico":
        if tipo == "turista":
            sort_key = "n_fotos_local"
        else:
            sort_key = "n_fotos_turistico"
    else:
        if tipo == "local":
            sort_key = "n_fotos_local"
        else:
            sort_key = "n_fotos_turistico"

    reverse_order = True

    def obtener_candidatos(nivel):
        candidatos = []

        for municipio, info in island_data.items():
            muni_clean = municipio.lower().strip()

            if residencia_clean and muni_clean == residencia_clean:
                continue

            if info.get("nivel_turistico") == nivel:
                candidatos.append((municipio, info))

        return sorted(
            candidatos,
            key=lambda x: x[1].get(sort_key, 0),
            reverse=reverse_order
        )

    seleccion = []
    fallback_usado = False

    for nivel in niveles_busqueda:
        candidatos = obtener_candidatos(nivel)

        for c in candidatos:
            if c not in seleccion and len(seleccion) < 3:
                seleccion.append(c)
                if nivel != nivel_objetivo:
                    fallback_usado = True

        if len(seleccion) >= 3:
            break

    if not seleccion:
        candidatos_all = [
            (m, info) for m, info in island_data.items()
            if not (residencia_clean and m.lower().strip() == residencia_clean)
        ]

        seleccion = sorted(
            candidatos_all,
            key=lambda x: x[1].get(sort_key, 0),
            reverse=reverse_order
        )[:3]

        fallback_usado = True

    if not seleccion:
        return {"error": "No hay municipios disponibles fuera de tu residencia."}

    principal = seleccion[0]
    alternativas = seleccion[1:3]

    return {
        "municipio": principal[0],
        "info": principal[1],
        "alternativas": [
            {"municipio": m, "info": i} for m, i in alternativas
        ],
        "nivel_objetivo": nivel_objetivo,
        "fallback_usado": fallback_usado,
        "tipo_usuario": tipo,
        "ambiente": ambiente,
        "isla": island,
        "residencia_detectada": municipio_residencia
    }