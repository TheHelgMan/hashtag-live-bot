import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROUP_ID = int(os.environ.get("GROUP_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋\n\n"
        "Это бот для предложок проекта «Живём» — медиапроекта который объясняет сложные вещи простыми словами.\n\n"
        "Есть идея для материала? Хочешь поделиться своей историей? Просто напиши сюда — мы читаем всё 🙏\n\n"
        "Анонимность: если хочешь остаться анонимным — просто не указывай своё имя в тексте."
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
    
    await context.bot.send_message(chat_id=GROUP_ID, text=forward_text)
    await update.message.reply_text(
        "Спасибо! Мы получили твою идею и рассмотрим её 🙏"
    )

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
