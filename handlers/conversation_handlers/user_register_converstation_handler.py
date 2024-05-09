from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler
from models.user import User

STATE_FIRST_NAME, STATE_LAST_NAME, STATE_PHONE_NUMBER, STATE_EMAIL = range(4)


class UserRegisterConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('user_register', cls.user_register)],
            states={
                STATE_FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, cls.first_name)],
                STATE_LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, cls.last_name)],
                STATE_PHONE_NUMBER: [
                    MessageHandler(filters.CONTACT, cls.phone_number),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, cls.phone_number),
                ],
                STATE_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, cls.state_email)],
            },
            fallbacks=[CommandHandler('exit_user_register', cls.exit_user_register)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def user_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Введіть своє ім\'я:')

        return STATE_FIRST_NAME

    @staticmethod
    async def first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
        first_name = update.message.text

        context.user_data['first_name'] = first_name

        await update.message.reply_text(f'Введіть своє прізвище:')

        return STATE_LAST_NAME

    @staticmethod
    async def last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
        first_name = update.message.text

        context.user_data['last_name'] = first_name

        contact_keyboard = KeyboardButton(text="Поділитись контактом", request_contact=True)
        keyboard = [
            [contact_keyboard],
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f'Поділіться своїми контактами або введіть номе телефону у форматі "380-(00)-000-00-00":',
            reply_markup=reply_markup
        )

        return STATE_PHONE_NUMBER

    @staticmethod
    async def phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.contact:
            context.user_data['phone_number'] = update.message.contact.phone_number
        else:
            context.user_data['phone_number'] = update.message.text

        await update.message.reply_text(f'Введіть свою поштову скриньку:')

        return STATE_EMAIL

    @classmethod
    async def state_email(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):

        first_name = context.user_data['first_name']
        last_name = context.user_data['last_name']
        phone_number = context.user_data['phone_number']
        email = update.message.text

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email
        )
        cls.session.add(new_user)
        cls.session.commit()

        await update.message.reply_text(
            f'Ви зареєстровані! \n'
            f'Ваше ім\'я: {first_name} \n'
            f'Ваше пірзвище: {last_name} \n'
            f'Ваш номер телефону: {phone_number} \n'
            f'Ваша електронна скринька: {email}'
        )

        return ConversationHandler.END

    @staticmethod
    async def exit_user_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Exit from conversation')

        return ConversationHandler.END