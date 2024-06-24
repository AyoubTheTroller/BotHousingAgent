from typing import List
from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
from telegram import constants
from app.service.mongodb.mongo_service import MongoService

class CommandHandlers:
    def __init__(self, mongo_service: MongoService):
        self.mongo_service = mongo_service

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    async def print_all_urls(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Retrieves and sends all URLs from MongoDB."""

        # Get the collection from the MongoService
        urls_collection = self.mongo_service.get_collection("urls_collection")

        # Find all documents in the collection
        urls = []

        #for document in urls_collection.find():
            #await context.bot.send_message(chat_id=update.effective_chat.id, text="url")

        print(constants.MessageLimit.MAX_TEXT_LENGTH)
        print(constants.MessageLimit)

        # Check for empty urls
        if not urls:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="No URLs found in the database."
            )
            return

    def get_handlers(self) -> List[CommandHandler]:
        """Returns a list of CommandHandler instances."""
        return [
            CommandHandler('start', self.start),
            CommandHandler('print_all_urls', self.print_all_urls)
            # ... add other CommandHandler instances here ...
        ]
