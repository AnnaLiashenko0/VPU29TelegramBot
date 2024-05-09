from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, \
    CallbackQueryHandler

from handlers.base_handler import BaseHandler

GENDER, PHOTO, AGE, BUTTON = range(4)


class FirstConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('begin', cls.begin)],
            states={
                GENDER: [MessageHandler(filters.Regex('^(Boy|Girl)$'), cls.gender)],
                PHOTO: [MessageHandler(filters.PHOTO, cls.photo)],
                AGE: [CallbackQueryHandler(cls.age)]
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Boy'), KeyboardButton('Girl')],
        ]
        reply_text = ReplyKeyboardMarkup(keyboard)
        await update.message.reply_text(f'Hello {update.effective_user.first_name}! Are you a Boy or a Girl?', reply_markup=reply_text)

        return GENDER

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Exit from conversation')

        return ConversationHandler.END

    @staticmethod
    async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
        gender = update.message.text
        context.user_data['gender'] = gender
        await update.message.reply_text(f'You are a {gender}. Share your photo, please!', reply_markup=ReplyKeyboardRemove())

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
    async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query
        await query.answer()

        age = query.data
        context.user_data['age'] = age

        await query.edit_message_text(text=f"You are {context.user_data['gender']}. Your age is {context.user_data['age']} years old.")

        return AGE