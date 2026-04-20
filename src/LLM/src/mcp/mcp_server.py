from src.LLM.src.mcp.tools_memory import tool_save_user_attribute
from src.LLM.src.mcp.tools_api import tool_get_island_data
from src.LLM.src.mcp.tools_recommender import tool_recommend_places
from src.LLM.src.mcp.tools_weather import tool_get_weather
from src.LLM.src.db.db_manager import get_user_profile
from src.LLM.src.mcp.tools_municipality_details import tool_get_municipality_details


async def call_mcp_tool(name, args):
    if name == "save_user_attribute":
        return await tool_save_user_attribute(
            user_id=args["user_id"],
            attribute=args["attribute"],
            value=args["value"],
            nombre=args.get("nombre")
        )

    if name == "get_island_data":
        return tool_get_island_data(args["island"])

    if name == "get_weather":
        return tool_get_weather(args["island"])

    if name == "get_municipality_details":
        island = args["island"]
        municipio = args["municipio"]
        island_data = tool_get_island_data(island)
        return tool_get_municipality_details(island_data, municipio)

    if name == "recommend_places":
        import time
        start_time = time.time()

        profile = get_user_profile(args["user_id"], nombre=args.get("nombre"))

        island_target = args["island"]
        island_data = tool_get_island_data(island_target)
        ambiente_act = args.get("ambiente", "estandar")

        muni_caliente = args.get("current_intent_muni")

        result = tool_recommend_places(
            user_profile=profile,
            island_data=island_data,
            user_id=args["user_id"],
            island=island_target,
            ambiente=ambiente_act,
            current_intent_muni=muni_caliente
        )

        tiempo_ms = round((time.time() - start_time) * 1000, 2)

        if "municipio" in result:
            municipio_principal = result["municipio"]
            alt1 = result["alternativas"][0]["municipio"] if len(result.get("alternativas", [])) > 0 else None
            alt2 = result["alternativas"][1]["municipio"] if len(result.get("alternativas", [])) > 1 else None

            await tool_save_user_attribute(
                user_id=args["user_id"],
                attribute="municipio_recomendado",
                value=municipio_principal,
                nombre=args.get("nombre")
            )

            await tool_save_user_attribute(
                user_id=args["user_id"],
                attribute="alternativa_1",
                value=alt1,
                nombre=args.get("nombre")
            )

            await tool_save_user_attribute(
                user_id=args["user_id"],
                attribute="alternativa_2",
                value=alt2,
                nombre=args.get("nombre")
            )

            await tool_save_user_attribute(
                user_id=args["user_id"],
                attribute="fecha_consulta",
                value=time.strftime("%Y-%m-%d %H:%M:%S"),
                nombre=args.get("nombre")
            )

            await tool_save_user_attribute(
                user_id=args["user_id"],
                attribute="tiempo_respuesta_ms",
                value=tiempo_ms,
                nombre=args.get("nombre")
            )
        return result