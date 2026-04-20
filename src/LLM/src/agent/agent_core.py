import json
from openai import OpenAI

from src.LLM.src.agent.prompts import SYSTEM_PROMPT
from src.LLM.src.agent.intent_classifier import classify_intent
from src.LLM.src.agent.context_manager import context_manager
from src.LLM.src.db.db_manager import (
    get_user_profile,
    create_empty_user,
    save_full_intent
)
from src.LLM.src.mcp.mcp_server import call_mcp_tool


client = OpenAI()


def inferir_nivel_intencion(tipo, ambiente, signals):

    if ambiente == "autentico":
        return 4 if tipo == "local" else 1

    if tipo == "local":
        return 1 if signals.get("muy_local") else 2

    return 3 if signals.get("evita_masas") else 4

class AgentCore:
    def __init__(self):
        self.context_manager = context_manager

    async def ask(self, user_id: str, message: str):

        if user_id not in context_manager.state:
            context_manager.state[user_id] = {
                "history": [],
                "current_name": None
            }

        intent = classify_intent(message)

        if intent.get("nombre"):
            context_manager.state[user_id]["current_name"] = intent["nombre"]

        active_name = context_manager.state[user_id].get("current_name")

        profile_prev = get_user_profile(user_id, nombre=active_name)
        tipo_prev = profile_prev.get("tipo")

        tipo_actual = (
            "local" if intent["is_local"]
            else "turista" if intent["is_tourist"]
            else tipo_prev
        )

        if not tipo_prev or (tipo_actual and tipo_actual != tipo_prev):
            new_name = create_empty_user(
                user_id,
                tipo_actual or "turista",
                nombre=active_name
            )
            context_manager.state[user_id]["current_name"] = new_name
            active_name = new_name

        nivel_intencion = inferir_nivel_intencion(
            tipo=tipo_actual,
            ambiente=intent["ambiente"],
            signals=intent["signals"]
        )

        if active_name:
            save_full_intent(
                user_id,
                active_name,
                {
                    "is_local": intent["is_local"],
                    "is_tourist": intent["is_tourist"],
                    "nombre": active_name,
                    "origin_city": intent.get("origin_city"),
                    "island": intent.get("island"),
                    "municipio": intent.get("municipio"),
                    "ambiente": intent.get("ambiente"),
                    "nivel_intencion": nivel_intencion,  # ✅ AQUÍ
                    "signals": intent.get("signals")
                }
            )

        profile = get_user_profile(user_id, nombre=active_name)
        data = profile.get("data", {})
        tipo_final = profile.get("tipo")
        ambiente_actual = data.get("ambiente", "estandar")

        target_island = (
            intent.get("island")
            or (data.get("isla_destino") if tipo_final == "turista"
                else data.get("isla_residencia"))
        )

        db_context = (
            f"ESTADO ACTUAL (BASE DE DATOS):\n"
            f"- Usuario: {active_name}\n"
            f"- Rol: {tipo_final}\n"
            f"- Isla: {target_island}\n"
            f"- Ambiente: {ambiente_actual}\n"
            f"- Municipio residencia: {data.get('municipio')}\n"
            f"- Nivel intención inferido: {data.get('nivel_intencion')}\n"
            f"- Señales: {data.get('signals')}\n"
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": db_context}
        ]

        messages.extend(context_manager.state[user_id]["history"])
        messages.append({"role": "user", "content": message})

        tools_definition = [{
            "type": "function",
            "function": {
                "name": "recommend_places",
                "description": (
                    "Recomienda municipios usándose el nivel de intención "
                    "inferido y almacenado en base de datos."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "island": {"type": "string"},
                        "ambiente": {"type": "string"}
                    },
                    "required": ["island"]
                }
            }
        }]

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools_definition,
                tool_choice={
                    "type": "function",
                    "function": {"name": "recommend_places"}
                }
            )

            msg = response.choices[0].message
            tool_results = []

            if msg.tool_calls:
                for call in msg.tool_calls:
                    args = json.loads(call.function.arguments)

                    args["user_id"] = user_id
                    args["nombre"] = active_name
                    args["ambiente"] = ambiente_actual
                    args["current_intent_muni"] = intent.get("municipio")

                    result = await call_mcp_tool(call.function.name, args)

                    if isinstance(result, tuple):
                        result = result[0]

                    tool_results.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    })

                final_res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages + [msg] + tool_results,
                    temperature=0
                )

                res_message = final_res.choices[0].message
            else:
                res_message = msg

            context_manager.state[user_id]["history"].append(
                {"role": "user", "content": message}
            )
            context_manager.state[user_id]["history"].append(
                {"role": "assistant", "content": res_message.content}
            )

            return res_message, tool_results

        except Exception as e:
            print(f"[AgentCore ERROR]: {e}")
            return (
                type(
                    "obj",
                    (object,),
                    {"content": "Lo siento, hubo un problema procesando tu solicitud."}
                ),
                []
            )