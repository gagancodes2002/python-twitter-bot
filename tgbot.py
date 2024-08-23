from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual token
TOKEN = '6527071707:AAEfnEn6IvArtSSSazkeSGd64-NKDMhoXlY'

# Path to the text file
import os

file_path = os.path.join(os.path.dirname(__file__), 'assets/client_1/tweetLinks.txt')

def read_lines():
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

chat_intervals = {}

async def send_line(context: CallbackContext):
    job = context.job
    lines = read_lines()
    chat_id = job.data['chat_id']
    current_index = job.data['current_index']

    if current_index < len(lines):
        await context.bot.send_message(chat_id=chat_id, text=lines[current_index])
        job.data['current_index'] += 1
    else:
        job.data['current_index'] = 0  # Reset index if you want to restart sending

async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    if chat_id not in chat_intervals:
        await update.message.reply_text("Starting to send lines...")
        job = context.job_queue.run_repeating(send_line, interval=180, first=0, data={'chat_id': chat_id, 'current_index': 0})
        chat_intervals[chat_id] = job
    else:
        await update.message.reply_text("Already sending lines. Use /stop to stop.")

async def stop(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    if chat_id in chat_intervals:
        job = chat_intervals.pop(chat_id)
        job.schedule_removal()
        await update.message.reply_text("Stopped sending lines.")
    else:
        await update.message.reply_text("No active line sending session.")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))

    application.run_polling()

if __name__ == '__main__':
    main()
