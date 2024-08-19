from aiogram import Bot
from app.telegram.loader.base_loader import BaseLoader
from app.service.mongodb.dao.user.user_dao import UserDAO

class AdminTriggeredNotificationEvent:
    def __init__(self, loader: BaseLoader, admin_dao: UserDAO, bot: Bot):
        self.loader = loader
        self.admin_dao = admin_dao
        self.bot = bot

    async def new_user_subscription(self, event_data: dict) -> None:
        admin = await self.admin_dao.get_user_by_username(event_data['admin_username'])
        not_set = await self.loader.get_message_template_by_lang(admin.language,"not_set")
        username = event_data['username'] or not_set
        first_name = event_data['first_name'] or not_set
        last_name = event_data['last_name'] or not_set
        id_or_username = event_data['username'] or event_data['id']
        message = await self.loader.get_message_template_by_lang(admin.language, "new_user_subscription",
                                                                 username=username,
                                                                 first_name=first_name,
                                                                 last_name=last_name,
                                                                 id_or_username=id_or_username)
        await self.bot.send_message(chat_id=admin.id, text=message)
