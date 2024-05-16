from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler

from handlers.base_handler import BaseHandler


class HtmlHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        app.add_handler(CommandHandler('html', cls.callback))

    @staticmethod
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = (
          "<b>Hello world</b>\n"
          "<i>Hello world</i>\n"
          '<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>\n'
          "<a href='https://vpu29.lviv.ua/'>VPU29</a>\n"
          "<u>Hello world</u>"

        )
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)


