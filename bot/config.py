"""Bot configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8639775102:AAGXojKkcgzyONMSc02UP1o3N2KtkE7f-EQ")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7924294552"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1003993864640"))
LOGS_CHANNEL_ID = int(os.getenv("LOGS_CHANNEL_ID", "-1004462118091"))

WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-frontend-url.vercel.app")
