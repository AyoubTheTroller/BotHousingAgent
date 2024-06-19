import logging
from telegram import Update
from telegram.ext import Application, ContextTypes

class TelegramApplication:

    def __init__(self, command_handlers):
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
        self.logger.debug("Telegram Application Started!")
        self.application = {}
        self.command_handlers = command_handlers

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    def register_handlers(self):
        handlers = self.command_handlers.get_handlers()
        for handler in handlers:
            self.application.add_handler(handler)

    def run_app(self, application: Application):
        self.application = application
        self.register_handlers()
        self.application.run_polling()
