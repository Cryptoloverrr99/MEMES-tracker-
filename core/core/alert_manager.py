from telegram import Bot
from telegram.constants import ParseMode
from config import settings, api_keys
import logging

class AlertManager:
    def __init__(self):
        self.bot = Bot(token=api_keys.TELEGRAM_BOT_TOKEN)
        self.logger = logging.getLogger(__name__)

    async def send_alert(self, token_data, dex_paid, dev_sold):
        message = (
            f"🚨 **New MEME Alert** 🚨\n\n"
            f"• Token: [{token_data['symbol']}]({token_data['url']})\n"
            f"• Market Cap: ${token_data['marketCap']:,.0f}\n"
            f"• Liquidity: ${token_data['liquidity']:,.0f}\n"
            f"• Volume 24h: ${token_data['volume']:,.0f}\n"
            f"• Dex Paid: {dex_paid.upper()}\n"
            f"• Dev Sold: {dev_sold.upper()}\n"
        )
        
        try:
            await self.bot.send_message(
                chat_id=api_keys.TELEGRAM_CHAT_ID,
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            self.logger.error(f"Failed to send alert: {str(e)}")

    async def send_error_alert(self, error_details):
        message = f"🔥 **CRASH DU BOT** 🔥\n\n```\n{error_details}\n```"
        await self.bot.send_message(
            chat_id=api_keys.TELEGRAM_CHAT_ID,
            text=message,
            parse_mode=ParseMode.MARKDOWN
          )
