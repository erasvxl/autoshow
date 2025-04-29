# bot/apps.py
import os
import asyncio
from threading import Thread
from django.apps import AppConfig
from django.conf import settings
from telegram.ext import ApplicationBuilder, CommandHandler

class BotConfig(AppConfig):
    name = 'bot'

    def ready(self):
        # Только в основном процессе Django runserver
        if os.environ.get('RUN_MAIN') != 'true':
            return
        print("🔔 BotConfig.ready() — запускаем Telegram-бота")

        from .handlers import start, help_command

        app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))

        def _run():
            # Создаём и устанавливаем event loop для этого потока
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(app.run_polling())
            finally:
                loop.close()

        Thread(target=_run, daemon=True).start()
