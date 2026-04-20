import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

API_BASE_URL = os.getenv("API_BASE_URL")

DB_PATH = os.getenv("DB_PATH", "")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")