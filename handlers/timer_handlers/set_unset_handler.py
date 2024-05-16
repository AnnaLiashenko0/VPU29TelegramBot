from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from handlers.base_handler import BaseHandler



class SetUnsetHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        app.add_handler(CommandHandler(["timer", "help"], cls.start))
        app.add_handler(CommandHandler("set", cls.set_timer))
        app.add_handler(CommandHandler("unset", cls.unset))

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends explanation on how to use the bot."""
        await update.message.reply_text("Hi! Use /set <seconds> to set a timer")

    @staticmethod
    async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send the alarm message."""
        job = context.job
        await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")

    @staticmethod
    async def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Remove job with given name. Returns whether job was removed."""
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True

    @staticmethod
    async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Add a job to the queue."""
        chat_id = update.effective_message.chat_id
        try:
            due = float(context.args[0])
            if due < 0:
                await update.effective_message.reply_text("Sorry we can not go back to future!")
                return

            job_removed = SetUnsetHandler.remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_once(SetUnsetHandler.alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

            text = "Timer successfully set!"
            if job_removed:
                text += " Old one was removed."
            await update.effective_message.reply_text(text)

        except (IndexError, ValueError):
            await update.effective_message.reply_text("Usage: /set <seconds>")

    @staticmethod
    async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Remove the job if the user changed their mind."""
        chat_id = update.message.chat_id
        job_removed = SetUnsetHandler.remove_job_if_exists(str(chat_id), context)
        text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
        await update.message.reply_text(text)