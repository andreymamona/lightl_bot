import os
import aioredis
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis = aioredis.from_url("redis://localhost")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Message from chat {update.effective_chat.id} user: {update.effective_user.name}")
    # tmp = await redis.get("chats")
    # if update.effective_chat.id not in tmp:
    #     await redis.lpush("chats", update.effective_chat.id)
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name} ({update.effective_chat.id})"
    )
    # print(tmp)
    # for i in redis.llen("chats"):


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Message from chat {update.effective_chat.id} user: {update.effective_user.name}")
    await update.message.reply_text(
        f"Hello {update.effective_user.last_name} ({update.effective_chat.id})"
    )


async def send_message(chat_id: int, text: str) -> None:
    bot = Bot(BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=text)


async def send_message_to_all(text: str) -> None:
    result = []
    for index in range(0, await redis.llen("chats")):
        chat_id = await redis.lindex("chats", index)
        result.append(chat_id)

    for chat_id in set(result):
        await send_message(chat_id=int(chat_id), text=text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(~filters.COMMAND, message))
    app.run_polling()
