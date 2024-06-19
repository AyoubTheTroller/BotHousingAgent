from typing import List
from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
from app.service.mongodb.mongo_service import MongoService

class CommandHandlers:
    def __init__(self, mongo_service: MongoService):  # Remove application here
        self.mongo_service = mongo_service

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    # ... other command handler methods ...

    def get_handlers(self) -> List[CommandHandler]:
        """Returns a list of CommandHandler instances."""
        return [
            CommandHandler('start', self.start),
            # ... add other CommandHandler instances here ...
        ]
