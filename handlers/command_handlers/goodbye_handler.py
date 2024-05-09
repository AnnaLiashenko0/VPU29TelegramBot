from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from handlers.base_handler import BaseHandler


class GoodbyeHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        app.add_handler(CommandHandler('goodbye', cls.callback))

    @staticmethod
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        last_name = update.effective_user.last_name
        if last_name is None:
            await update.message.reply_text(f'Bye {update.effective_user.first_name}!')

        else:
            await update.message.reply_text(f'Bye {update.effective_user.first_name} {last_name}!')