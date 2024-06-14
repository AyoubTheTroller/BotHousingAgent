import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

class TelegramApplication:

    def __init__(self, token_api):
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
        self.logger.debug("Telegram Application Started!")

        application = ApplicationBuilder().token(token_api).build()
        start_handler = CommandHandler('start', self.start)
        application.add_handler(start_handler)

        application.run_polling()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
