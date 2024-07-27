from aiogram import Bot
from app.telegram.notification.loader import NotificationLoader
from app.service.mongodb.dao.user.user_dao import UserDAO

class AdminTriggeredNotificationEvent:
    def __init__(self, loader: NotificationLoader, admin_dao: UserDAO, bot: Bot):
        self.loader = loader
        self.admin_dao = admin_dao
        self.bot = bot

    async def new_user_subscription(self, event_data: dict) -> None:
        admin = await self.admin_dao.get_user_by_username(event_data['admin_username'])
        message = await self.loader.get_message_template("new_user_subscription", admin.language, user_username=event_data['user_username'])
        await self.bot.send_message(chat_id=admin.user_id, text=message)
