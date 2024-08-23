import random
from twikit import Client
from sqlite3 import connect
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from time import sleep


account_list = [ 
    {
        "name": "Spectra",
        "username": "Spectra",
        "password": "Spectra",
        "email": "Spectra",
        "token": "6a300b9999eef2f148ba148c00dae518af6adb3569cb86fe151dec25f001ea2c1bbe84a3b093240828911e174f5c4af65c1f96117fd51e450bb16ef8df89c3f8a722103ad7b59de05790b5f8474dc7df",
        "auth_token": "74e269365b1ea4d049056ecb8d97710fe5e08eed",
    }
]
    

def get_reply_ids_from_users(client_name, db_path, accounts_list):
    try:
        commentable_ids = []
        connection = connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM todo_client WHERE name = ?", (client_name,))
        client_row = cursor.fetchall()
        commentable_accounts = client_row[0][2].split("\n")
        # strip all the white spaces
        commentable_accounts = [account.strip() for account in commentable_accounts]
        print("Commentable Accounts: ", commentable_accounts)
        
        # scraper_account = random.choice(commentable_accounts)
        scraper_account = random.choice(accounts_list)
        print("Scraper Account: ", scraper_account)
        # make 6 char length session_id using obj['username'] as the seed
        session_id =  scraper_account['username'][:6]
        client = Client('en-US', proxy='http://user_3cca1a,type_residential,session_{username}:ironman2002@portal.anyip.io:1080'.format(username=session_id), timeout=None)
        client.set_cookies(
            {
             'auth_token': scraper_account['auth_token'],
                'ct0': scraper_account['token']
            }
        )
        for account in commentable_accounts:
            print("Account: ", account)
            tweets = client.get_user_by_screen_name(account).get_tweets(tweet_type="Tweets", count=1)
            # tweets = client.get_user_tweets(user_id=account ,tweet_type="Tweets", count=1)
            if tweets:
                commentable_ids.append(tweets[0].id)
        print("Commentable IDs: ", commentable_ids)
        return commentable_ids
    except Exception as e:
        print("Exception S: ", e)
        

def get_replies_ids(reply_type, client_name, db_path, accounts_list):
    try:
        commentable_ids = []
        connection = connect(db_path)
        cursor = connection.cursor()
        if reply_type == "1":
            cursor.execute("SELECT * FROM todo_client WHERE name = ?", (client_name,))
            client_row =  cursor.fetchall()
            commentable_ids = client_row[0][3].split("\n")
            # strip all the white spaces
            commentable_ids = [account.strip() for account in commentable_ids]
            return commentable_ids
        elif reply_type == "2":
            return get_reply_ids_from_users(client_name, db_path, accounts_list)
    except Exception as e:
        print("Exception T: ", e)

# print(get_replies_ids("1", "Spectra", "db.sqlite3", account_list))

def tweet(obj, message, client_name, db_path, use_images, replie_ids):
    
    print("Replies in tweet func : ", replie_ids)
    try:
        reply_to_id = None
        if len(replie_ids) > 0:
           reply_to_id = random.choice(replie_ids)
           print("Replying to: ", reply_to_id)
        else:
           print("No replies")
        media_ids = []
        
        # Make a new database connection and cursor within each thread
        connection = connect(db_path)
        cursor = connection.cursor()
        
        # make 6 char length session_id using obj['username'] as the seed
        session_id =  obj['username'][:6]
        client = Client('en-US', proxy='http://user_3cca1a,type_residential,session_{username}:ironman2002@portal.anyip.io:1080'.format(username=session_id), timeout=None)
        client.set_cookies(
            {
             'auth_token': obj['auth_token'],
             'ct0': obj['token']
            }
        )
        # get the image from the database
        if use_images:
           cursor.execute(f"SELECT * FROM todo_image WHERE client_link_id = {1}")
           images = cursor.fetchall()
           random_image = images[random.randint(0, len(images)-1)]
           media_ids.append(client.upload_media(random_image[2]))
        # add a random 5 alphanumeric string to the message
        message = message + " " + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=5))
        tweet_id = client.create_tweet(message, media_ids=media_ids, reply_to=reply_to_id)
        if tweet_id.id:
            tweet_link = "https://twitter.com/{username}/status/{tweet_id.id}".format(username=obj['username'], tweet_id=tweet_id)
            cursor.execute("SELECT tweet_links FROM todo_client WHERE name = ?", (client_name,))
            tweet_links = cursor.fetchone()
            tweet_links = tweet_links[0] if tweet_links else ''
            tweet_links = tweet_links + "\n" + tweet_link
            cursor.execute("UPDATE todo_client SET tweet_links = ? WHERE name = ?", (tweet_links, client_name))
            connection.commit()
            # Close the cursor and connection
            cursor.close()
            connection.close()
            return True  # Tweet successful
        else:
            return False  # Tweet failed

    except Exception as e:
        print('Exception B : {dikkat}'.format(dikkat=e))                                               
        return False  # Tweet failed

def tweet_wrapper(args):
    return tweet(*args)


        


def tweets(tweet_list, accounts_list, client, db_path, iteration, use_images, action):
    
    reply_ids = []
    
    if action == "Comment" or action == "Mixed":
        # 1 for comments, 2 for users
        reply_type = input("Reply to \n1. Comments\n2. Users\nEnter Reply Type: ")
        reply_ids = get_replies_ids(reply_type, client,db_path, accounts_list)
        print("Reply IDs: ", reply_ids)
    
    print("Reply IDs After: ", reply_ids)
    # Initialize variables to track success and error counts
    success_count = 0
    error_count = 0
    
    # Initialize the progress bar
    progress_bar = tqdm(total=iteration, desc="Tweeting", unit=" tweet", colour="green")
    
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
        # Prepare arguments for the tweet function
        # args = [(random.choice(accounts_list), random.choice(tweet_list), client, db_path, use_images, reply_ids if  random_action else []) for _ in range(iteration)]
        
        # if action == "Mixed" then we should randomly sometimes give reply_ids and sometimes empty list
        if action == "Mixed":
            args = [(random.choice(accounts_list), random.choice(tweet_list), client, db_path, use_images, reply_ids if random.choice([True, False]) else []) for _ in range(iteration)]
        else:
            args = [(random.choice(accounts_list), random.choice(tweet_list), client, db_path, use_images, reply_ids) for _ in range(iteration)]
        
        # Map the tweet function to the arguments using ThreadPoolExecutor
        for result in executor.map(tweet_wrapper, args):
            if result:
                success_count += 1
            else:
                error_count += 1
            progress_bar.update(1)  # Update progress for each tweet
            sleep(0.5)  # Simulate tweet processing time
        # Close the progress bar
        progress_bar.close()
    
    # Display success rate and error count
    total_tweets = success_count + error_count
    print(f"Total tweets: {total_tweets}")
    print(f"Successful tweets: {success_count}")
    print(f"Failed tweets: {error_count}")

__all__ = ['tweet', 'tweets']
