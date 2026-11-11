import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = "9032744181:AAGBxhKFj-WGEW31AVk_p7VqNOAUkQQkKuI"
SOURCE_ID = -1004431649167
TARGET_ID = -5406590761

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

async def fwd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post and update.channel_post.chat.id == SOURCE_ID:
        try:
            await context.bot.forward_message(
                chat_id=TARGET_ID,
                from_chat_id=SOURCE_ID,
                message_id=update.channel_post.message_id
            )
            print(f"메시지 전달 성공! (ID: {update.channel_post.message_id})")
        except Exception as e:
            print(f"전달 실패: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.Chat(SOURCE_ID), fwd))
    print("🚀 자동 전달 봇 작동 시작!")
    app.run_polling()