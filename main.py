import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROUP_ID = int(os.environ.get("GROUP_ID"))
THREAD_ID = int(os.environ.get("THREAD_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋\n\n"
        "Это бот для предложок проекта «Живём».\n\n"
        "Есть идея для материала? Просто напиши сюда — мы читаем всё 🙏\n\n"
        "Если хочешь остаться анонимным — не указывай своё имя в тексте."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    
    user = update.message.from_user
    text = update.message.text or ""
    username = f"@{user.username}" if user.username else user.full_name
    
    forward_text = (
        f"📬 Новая предложка для #Живём\n\n"
        f"От: {username}\n\n"
        f"💬 {text}"
    )
    
    try:
        await context.bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=THREAD_ID,
            text=forward_text
        )
        logging.info(f"Отправлено в группу {GROUP_ID} тред {THREAD_ID}")
        await update.message.reply_text("Спасибо! Мы получили твою идею 🙏")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
