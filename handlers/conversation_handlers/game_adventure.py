from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler

ACQUAINTANCE, CHOICE, END = range(3)


class GameConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('startgame', cls.startgame)],
            states={
                ACQUAINTANCE: [MessageHandler(filters.Regex('^(Так|Ні)$'), cls.acquaintance)],
                CHOICE: [MessageHandler(filters.Regex('^(1|2)$'), cls.choice)],
                END: [MessageHandler(filters.Regex('^Відправити$'), cls.end)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Так'), KeyboardButton('Ні')],
        ]

        reply_text = ReplyKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Привіт {update.effective_user.first_name}!)) давай зіграємо?",reply_markup=reply_text)

        return ACQUAINTANCE

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Вихід')

        return ConversationHandler.END

    @staticmethod
    async def acquaintance(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Так':
            keyboard = [
                [KeyboardButton('1'), KeyboardButton('2')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard)
            await update.message.reply_text(
            f"""
             приступим до першого завдання,
в тебе є вибір.)))
 1.Напиши мені "Номер карти , Термін дії , CVC2"(якщо у тебе ще нема, то можна одного з батьків)                
 2.Виріж на руці весь код цієї гри(87 рядків коду...)  
            """, reply_markup=reply_text)

            return CHOICE
        elif answer == 'Ні':
            await update.message.reply_text(f'Тобі не цікаво що за гра?:)))')
            return ConversationHandler.END




    @staticmethod
    async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == '1':
            keyboard = [
                [KeyboardButton('Відправити')]
            ]

            reply_text = ReplyKeyboardMarkup(keyboard)
            await update.message.reply_text(
            f"""
           Ти майже пройшов гру!!))
 Щоб перемогти тобі потрібно відправити код, який прийшов тобі в смс))))
                """, reply_markup=reply_text)
            return END
        elif answer == '2':
            await update.message.reply_text(f'ти помер')
            return ConversationHandler.END
    @staticmethod
    async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            await update.message.reply_text(f'Молодець! Гру завершено')
            return ConversationHandler.END
