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
        await update.message.reply_text(f'You BAD {update.message.text}. Share your hot photo!')

        return PHOTO

    @staticmethod
    async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Sends a message with three inline buttons attached."""
        keyboard = [
            [
                InlineKeyboardButton("1", callback_data="1"),
                InlineKeyboardButton("2", callback_data="2"),
            ],
            [
                InlineKeyboardButton("3", callback_data="3"),
                InlineKeyboardButton("4", callback_data="4"),
            ],
            [
                InlineKeyboardButton("5", callback_data="5"),
                InlineKeyboardButton("6", callback_data="6"),
            ],
            [
                InlineKeyboardButton("7", callback_data="7"),
                InlineKeyboardButton("8", callback_data="8"),
            ],
            [
                InlineKeyboardButton("9", callback_data="9"),
                InlineKeyboardButton("10", callback_data="10"),
            ],
            [
                InlineKeyboardButton("11", callback_data="11"),
                InlineKeyboardButton("12", callback_data="12"),
            ],
            [
                InlineKeyboardButton("13", callback_data="13"),
                InlineKeyboardButton("14", callback_data="14"),
            ],
            [
                InlineKeyboardButton("15", callback_data="15"),
                InlineKeyboardButton("16", callback_data="16"),
            ],
            [
                InlineKeyboardButton("17", callback_data="17"),
                InlineKeyboardButton("18", callback_data="18"),
            ],
            [
                InlineKeyboardButton("19", callback_data="19"),
                InlineKeyboardButton("20", callback_data="20"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Thank you for your photo! How old are you?)", reply_markup=reply_markup)

        return AGE

    @staticmethod
    async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        await query.answer()

        await query.edit_message_text(text=f"Your age is: {query.data}")

        return ConversationHandler.END