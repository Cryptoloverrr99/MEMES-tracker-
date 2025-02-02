import socket
from telegram import Bot
from config import api_keys

class HealthMonitor:
    @staticmethod
    async def send_report():
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        message = f"📊 **Bot Status**\n• Host: {hostname}\n• IP: {ip}"
        
        await Bot(token=api_keys.TELEGRAM_BOT_TOKEN).send_message(
            chat_id=api_keys.TELEGRAM_CHAT_ID,
            text=message
        )
