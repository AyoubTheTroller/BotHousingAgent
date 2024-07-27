from aiogram import Bot
from app.telegram.notification.loader import NotificationLoader
from app.service.mongodb.dao.user.user_dao import UserDAO

class TriggeredNotificationEvent:
    def __init__(self, loader: NotificationLoader, user_dao: UserDAO, bot: Bot):
        self.loader = loader
        self.user_dao = user_dao
        self.bot = bot

    async def user_approved(self, event_data: dict) -> None:
        user_language = await self.user_dao.get_user_language_by_id(event_data['user_id'])
        message = await self.loader.get_message_template("user_approved", user_language, admin_username=event_data['admin_username'])
        await self.bot.send_message(chat_id=event_data['user_id'], text=message)
