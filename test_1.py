from random import randint, shuffle, uniform
from sqlite3 import connect
import time
import schedule
from actions import bot

# Connect to the database
connection = connect('db.sqlite3')
cursor = connection.cursor()

# Step 1: Ask user for selection of batch
print("\nSelect Batch")
cursor.execute("SELECT * FROM todo_account")
batches = cursor.fetchall()

for index, batch in enumerate(batches):
    print(f"{index+1}. {batch[3]}")
batch_selection = int(input("Enter Batch Number: "))
selected_batch = batches[batch_selection-1]
print(selected_batch)

# Step 2: Ask user for selection of client
print("\nSelect Client")
cursor.execute(f"SELECT * FROM todo_client")
clients = cursor.fetchall()

for index, client in enumerate(clients):
    print(f"{index+1}. {client[1]}")
client_selection = int(input("Enter Client Number: "))
selected_client = clients[client_selection-1]
print(selected_client)

# Step 3: Ask user for selection of action
print("\nSelect Action")
actions = ["Tweet", "Comment", "Mixed"]
for index, action in enumerate(actions):
    print(f"{index+1}. {action}")
action_selection = int(input("Enter Action Number: "))
selected_action = actions[action_selection-1]
print(selected_action)

# Step 3.1: Ask user if images are to be used and percentage
use_images = input("Use Images? (y/n): ").lower() == 'y'
if use_images:
    image_percentage = int(input("Enter the percentage of actions to include images (0-100): "))
    if not (0 <= image_percentage <= 100):
        raise ValueError("Percentage must be between 0 and 100.")
else:
    image_percentage = 0
print(use_images, image_percentage)

# Step 4: Ask user number of tweets/comments to make
number_of_actions = int(input("Enter Number of Actions: "))
print(number_of_actions)

# Commit the changes to the database
cursor.connection.commit()

def schedule_action(selected_batch, selected_client, selected_action, cursor, start, end, client_content_list, filtered_accounts_list, number_of_actions, image_percentage):
    # Randomize the interval slightly
    interval_minutes = randint(start, end)
    print("Interval: ", interval_minutes)

    # Add a random delay before performing the action
    delay_seconds = uniform(2, 7)  # Random delay between 2 to 7 seconds
    time.sleep(delay_seconds)

    # Randomly determine the number of actions for this round to avoid detection
    actions_this_round = randint(1, number_of_actions)

    # Perform the action
    bot.tweets(client_content_list, filtered_accounts_list, selected_client[1], 'db.sqlite3', actions_this_round, image_percentage, selected_action)
    
    # Reschedule the action with a random interval
    schedule.every(interval_minutes).minutes.do(schedule_action, selected_batch, selected_client, selected_action, cursor, start, end, client_content_list, filtered_accounts_list, number_of_actions, image_percentage)

def run_action(selected_batch, selected_client, selected_action, cursor):
    filtered_accounts = selected_batch[2]
    filtered_accounts_list = []
    for account in filtered_accounts.split("\n"):
        parts = account.split(":")
        username = parts[0]
        email = parts[1]
        password = parts[2]
        token = parts[3]
        auth_token = parts[4]
        filtered_accounts_list.append({
            "email": email.strip(),
            "password": password.strip(),
            "username": username.strip(),
            "token": token.strip(),
            "auth_token": auth_token.strip()
        })
        
    client_content = selected_client[5]
    client_content_list = []
    for content in client_content.split("\n"):
        client_content_list.append(content)

    # Shuffle the filtered_accounts_list and client_content_list
    shuffle(filtered_accounts_list)
    shuffle(client_content_list)
    
    # Ask user if they want to run action immediately or schedule it
    print("Select type of execution")
    print("1. Immediate")
    print("2. Schedule")
    execution_type = int(input("Enter Execution Type: "))
    if execution_type == 1:
        bot.tweets(client_content_list, filtered_accounts_list, selected_client[1], 'db.sqlite3', number_of_actions, image_percentage, selected_action)
    else:
        print("Scheduling the action")
        start = int(input("Enter the start of the range for running the action (in minutes): "))
        end = int(input("Enter the end of the range for running the action (in minutes): "))
    
        # Schedule the action with a random interval within the range
        interval_minutes = randint(start, end)
        print("Interval: ", interval_minutes)
        schedule.every(interval_minutes).minutes.do(schedule_action, selected_batch, selected_client, selected_action, cursor, start, end, client_content_list, filtered_accounts_list, number_of_actions, image_percentage)
    
        # Infinite loop to keep the script running
        while True:
            schedule.run_pending()
            time.sleep(1)

# Execute the action
run_action(selected_batch, selected_client, selected_action, cursor)
