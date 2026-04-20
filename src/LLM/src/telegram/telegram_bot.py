from telegram.ext import Application, CommandHandler, MessageHandler, filters
from src.LLM.src.agent.agent_core import AgentCore
from src.LLM.src.config import TELEGRAM_BOT_TOKEN
import json
import re

agent = AgentCore()

def markdown_links_to_html(text: str) -> str:

    pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    return re.sub(pattern, r'<a href="\2">\1</a>', text)


async def start(update, context):
    user_id = str(update.message.chat_id)

    agent.context_manager.clear_user(user_id)
    print(f"[BOT] Contexto de memoria volátil reseteado para: {user_id}")

    await update.message.reply_text(
        "🌴✨ <b>¡Hola!</b> Soy <b>Canarias Recommender</b>, tu guía personal para descubrir las Islas Canarias de una forma única y a tu medida.\n\n"
        "Conozco cada isla, sus municipios y la forma en la que se viven realmente. "
        "Dime si eres local o visitante y qué te apetece hoy, y me encargaré de recomendarte "
        "lugares que encajen contigo.\n\n"
        "💬 <b>Puedes hablar conmigo de forma natural</b>, por ejemplo:\n"
        "• Quiero sitios muy locales\n"
        "• No me gustan los lugares masificados\n"
        "• Quiero vivir la isla como un turista / como un canario más\n\n"
        "Cuando quieras, empezamos 😊",
        parse_mode="HTML"
    )


async def user_message(update, context):
    user_id = str(update.message.chat_id)
    text = update.message.text

    model_msg, tool_data = await agent.ask(user_id, text)

    if not model_msg or not hasattr(model_msg, "content"):
        await update.message.reply_text(
            "Lo siento, he tenido un problema interno al procesar tu mensaje."
        )
        return

    content = model_msg.content.strip()

    clean_content = re.sub(r'^```json\s*|```\s*$', '', content, flags=re.MULTILINE).strip()

    if clean_content.startswith("[") and clean_content.endswith("]"):
        try:
            mensajes = json.loads(clean_content)
            if isinstance(mensajes, list):
                for msg_text in mensajes:
                    if msg_text.strip():
                        msg_text = markdown_links_to_html(msg_text)
                        await update.message.reply_text(msg_text, parse_mode="HTML")
                return
        except Exception as e:
            print(f"[BOT ERROR] Error al parsear JSON: {e}")

    if content.startswith("{") and content.endswith("}"):
        await update.message.reply_text(
            "Estoy preparando la mejor recomendación para ti 😊"
        )
        return

    content = markdown_links_to_html(content)
    await update.message.reply_text(content, parse_mode="HTML")

def init_bot():
    print("[BOT] Iniciando aplicación de Telegram con Sistema Experto…")

    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .read_timeout(60)
        .write_timeout(60)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_message))

    print("[BOT] ON ✅ Sistema listo para recomendaciones por clusters…")
    app.run_polling()