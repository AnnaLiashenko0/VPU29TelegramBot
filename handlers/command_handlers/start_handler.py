from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CommandHandler

from handlers.base_handler import BaseHandler


class StartHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        app.add_handler(CommandHandler('start', cls.callback))

    @staticmethod
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Share my location', request_location=True)],
            [KeyboardButton('Share my contact', request_contact=True)],
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I'm a bot, please talk to me!",
            reply_markup=reply_markup
        )