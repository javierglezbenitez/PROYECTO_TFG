def tool_get_municipality_details(island_data: dict, municipio: str):

    if municipio not in island_data:
        return {
            "error": f"El municipio '{municipio}' no existe en esta isla o no aparece en los datos."
        }

    return island_data[municipio]