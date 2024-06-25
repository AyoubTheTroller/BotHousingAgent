from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
from app.service.mongodb.mongo_service import MongoService
from app.service.template.template_service import TemplateService

class PrepareUrl():

    def __init__(self, mongo_service: MongoService, template_service: TemplateService):
        self.mongo_service = mongo_service
        self.template_service = template_service

    START, CITY, MAX_PRICE, ROOM_NUMBER, FURNISHED = range(5)

    async def prepare_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Starts the conversation to collect URL parameters."""
        await update.message.reply_text(
            self.template_service.render_telegram_template("conversation", "get_search_param", "start")
        )
        await update.message.reply_text(
            self.template_service.render_telegram_template("conversation", "get_search_param", "city")
        )
        return self.CITY  # Move to the next state to get the city

    async def get_city(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Gets the city from the user."""
        context.user_data['city'] = update.message.text
        await update.message.reply_text(
            self.template_service.render_telegram_template("conversation", "get_search_param", "max_price")
        )
        return ConversationHandler.END  # Move to the next state to get the max price

    def get_handler(self):
        return ConversationHandler(
                entry_points=[CommandHandler('prepare_url', self.prepare_url)],
                states={
                    self.CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_city)],
                },
                fallbacks=[],  # You might want to add fallbacks later
            )
