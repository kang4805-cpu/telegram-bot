import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Render 포트 바인딩용 더미 웹 서버 (서버가 꺼지는 것을 방지)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

BOT_TOKEN = "9032744181:AAEPqDw9HoCxV1w3eaWKQaP88w-7vE3KQ0"
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
    # 백그라운드 웹 서버 스레드 시작
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # 텔레그램 봇 실행
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.Chat(SOURCE_ID), fwd))
    print("🚀 클라우드 24시간 자동 전달 봇 작동 시작!")
    app.run_polling()