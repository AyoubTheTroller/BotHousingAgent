from aiogram import Bot
from app.telegram.handler.loader.components_loader import ComponentsLoader

class TriggeredNotificationEvent:
    def __init__(self, loader: ComponentsLoader, bot: Bot):
        self.loader = loader
        self.bot = bot

    async def base_notification(self, event_data: dict, bot: Bot) -> None:
        user_id = event_data['user_id']
        message = event_data['message']
        await bot.send_message(chat_id=user_id, text=message)

    async def user_approved(self, event_data: dict) -> None:
        user_id = event_data['user_id']
        message = self.loader.get_message_template("user_approved", admin_username=event_data['admin_username'])
        await self.bot.send_message(chat_id=user_id, text=message)
