from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import time

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with the token you got from @BotFather
TOKEN = '6527071707:AAEfnEn6IvArtSSSazkeSGd64-NKDMhoXlY'

# Path to the text file
# backend\src\assets\client_1\tweetLinks.txt
file_path = os.path.join(os.path.dirname(__file__), 'data\client_data/client_1/tweetLinks.txt')

# Read the lines from the text file
def read_lines():
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

# Dictionary to keep track of intervals for each chat
chat_intervals = {}

# Function to send a line of text to a specified chat
def send_line(context: CallbackContext):
    job = context.job
    lines = read_lines()
    chat_id = job.context['chat_id']
    current_index = job.context['current_index']

    if current_index < len(lines):
        context.bot.send_message(chat_id=chat_id, text=lines[current_index])
        job.context['current_index'] += 1
    else:
        job.context['current_index'] = 0  # Reset index if you want to restart sending

# Command handler to start sending messages
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    if chat_id not in chat_intervals:
        context.bot.send_message(chat_id=chat_id, text="Starting to send lines...")
        job = context.job_queue.run_repeating(send_line, interval=180, first=0, context={'chat_id': chat_id, 'current_index': 0})
        chat_intervals[chat_id] = job
    else:
        context.bot.send_message(chat_id=chat_id, text="Already sending lines. Use /stop to stop.")

# Command handler to stop sending messages
def stop(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    if chat_id in chat_intervals:
        job = chat_intervals.pop(chat_id)
        job.schedule_removal()
        context.bot.send_message(chat_id=chat_id, text="Stopped sending lines.")
    else:
        context.bot.send_message(chat_id=chat_id, text="No active line sending session.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stop", stop))

    # Start polling for updates
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
