from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler


class LocationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        location_handler = MessageHandler(filters.LOCATION, cls.callback)
        app.add_handler(location_handler)

    @staticmethod
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        lat = update.message.location.latitude
        lon = update.message.location.longitude

        await update.message.reply_text(f'lat = {lat}, lon = {lon}')