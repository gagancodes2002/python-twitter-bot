from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, filters
from telegram.error import ChatMigrated
from sqlite3 import connect

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your token
TOKEN = '6527071707:AAEfnEn6IvArtSSSazkeSGd64-NKDMhoXlY'

# Function to read lines from the database
def read_lines():
    db = connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute("SELECT tweet_links FROM todo_client WHERE name = ?", ("Venko",))
    tweet_links = cursor.fetchall()
    tweet_links = tweet_links[0][0].split("\n")
    print("Tweet Links : ", tweet_links)
    tweet_links = [tweet_link.strip() for tweet_link in tweet_links]
    return tweet_links

# Dictionary to track intervals for each chat
chat_intervals = {}

# Function to send a line of text to a specified chat
async def send_line(context: CallbackContext):
    job = context.job
    lines = read_lines()
    chat_id = job.data['chat_id']
    current_index = job.data['current_index']

    if current_index < len(lines):
        message = lines[current_index].strip()  # Remove leading/trailing whitespace
        if message:  # Ensure the message is not empty
            try:
                await context.bot.send_message(chat_id=chat_id, text=message)
                job.data['current_index'] += 1
            except ChatMigrated as e:
                # Update the chat ID with the new ID
                new_chat_id = e.new_chat_id
                job.data['chat_id'] = new_chat_id
                chat_intervals[new_chat_id] = chat_intervals.pop(chat_id)
                await context.bot.send_message(chat_id=new_chat_id, text=message)
        else:
            job.data['current_index'] += 1  # Skip empty lines
            await send_line(context)  # Send the next line
    else:
        job.data['current_index'] = 0  # Reset index to restart sending
    job = context.job
    lines = read_lines()
    chat_id = job.data['chat_id']
    current_index = job.data['current_index']

    if current_index < len(lines):
        try:
            await context.bot.send_message(chat_id=chat_id, text=lines[current_index])
            job.data['current_index'] += 1
        except ChatMigrated as e:
            # Update the chat ID with the new ID
            new_chat_id = e.new_chat_id
            job.data['chat_id'] = new_chat_id
            chat_intervals[new_chat_id] = chat_intervals.pop(chat_id)
            await context.bot.send_message(chat_id=new_chat_id, text=lines[current_index])
    else:
        job.data['current_index'] = 0  # Reset index to restart sending

# Command handler to start sending messages
async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    if chat_id not in chat_intervals:
        await context.bot.send_message(chat_id=chat_id, text="Starting to send lines...")
        job = context.job_queue.run_repeating(send_line, interval=10, first=0, data={'chat_id': chat_id, 'current_index': 0})
        chat_intervals[chat_id] = job
    else:
        await context.bot.send_message(chat_id=chat_id, text="Already sending lines. Use /stop to stop.")

# Command handler to stop sending messages
async def stop(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    if chat_id in chat_intervals:
        job = chat_intervals.pop(chat_id)
        job.schedule_removal()
        await context.bot.send_message(chat_id=chat_id, text="Stopped sending lines.")
    else:
        await context.bot.send_message(chat_id=chat_id, text="No active line sending session.")

def main():
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))

    # Start polling for updates
    application.run_polling()

if __name__ == '__main__':
    main()