from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}! Я бот вашего Auto Show."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Я могу отправлять вам уведомления о новых заказах.\n\n"
        "Команды:\n"
        "/start — запустить бота\n"
        "/help — показать это сообщение"
    )
    await update.message.reply_text(text)
