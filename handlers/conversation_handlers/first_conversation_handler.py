from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, \
    CallbackQueryHandler

from handlers.base_handler import BaseHandler

GENDER, PHOTO, AGE = range(3)


class FirstConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('begin', cls.begin)],
            states={
                GENDER: [MessageHandler(filters.Regex('^(Boy|Girl)$'), cls.gender)],
                PHOTO: [MessageHandler(filters.PHOTO, cls.photo)],
                AGE: [CallbackQueryHandler(cls.age)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Hello {update.effective_user.first_name}! Are you a Boy or a Girl?')

        return GENDER

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Лівнув, БОТ!')

        return ConversationHandler.END


    @staticmethod
    async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'You very BAD {update.message.text}. Share your hot photo!')

        gender = update.message.text
        context.user_data['gender'] = gender

        return PHOTO

    @staticmethod
    async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Thank you for your photo! What's your age?")

        keyboard = []
        number = 1

        for i in range(10):
            row = []

            for j in range(5):
                row.append(InlineKeyboardButton(f"{number}", callback_data=f"{number}"))
                number += 1

            keyboard.append(row)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Choose your age:", reply_markup=reply_markup)

        return AGE


    @staticmethod
    async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query


        await query.answer()

        age = query.data

        context.user_data['age'] = age

        await query.edit_message_text(text=f"You are {context.user_data['gender']} gender. Your age is {context.user_data['age']} years old.")

        return ConversationHandler.END