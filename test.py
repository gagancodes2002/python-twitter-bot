from twikit import Client
import json
# import a file named accounts.txt
# read the file and store the contents in a variable


accounts = open('data/store/accounts.txt', 'r')
accounts = accounts.readlines()
accountsList = []
#  const parts = credential.split(":");
#     const email = parts[0];
#     const password = parts[1];
#     const username = parts[2];
#     const token = parts[3];
#     return { email, password, username, token };

accounts = [account.strip() for account in accounts]
for account in accounts:
    parts = account.split(":")
    email = parts[0]
    password = parts[1]
    username = parts[2]
    token = parts[3]
    auth_token = parts[4]
    accountsList.append({
        "email": email,
        "password": password,
        "username": username,
        "token": token,
        "auth_token": auth_token
    })
    

# accounts = [account.strip() for account in accounts]
# print(accounts)
# Initialize client

# pass proxy for HTTPClient in kwargs
# {'proxy': "http://user_3cca1a,type_residential,session_python:ironman2002@portal.anyip.io:1080"}
# client = Client('en-US',proxy='http://user_3cca1a,type_residential,session_python:ironman2002@portal.anyip.io:1080')



# # Login to the service with provided user credentials
# client.load_cookies(
#     path='cookies.json',
# )

# csrf =  client.create_tweet("Hello World 456")
# print(csrf)



def tweet(obj, message):
    # make 6 char length session_id using obj['username'] as the seed
    session_id =  obj['username'][:6]
    client = Client('en-US',proxy='http://user_3cca1a,type_residential,session_{username}:ironman2002@portal.anyip.io:1080'.format(username=session_id),timeout=None)
    client.set_cookies(
        {
         'auth_token': obj['auth_token'],
         'ct0': obj['token']
        }
    )
    
    client.create_tweet(message)
    

def tweets(list):
    # slice the accountsList to the length of the list
    currentAccounts = accountsList[:len(list)]
    for i in range(len(list)):
        tweet(currentAccounts[i], list[i])
        
# tweets(["Good morning, how are you doing today?" , "Hello World! Good Morning"])

tweet(accountsList[57], "Hello World! 3 Good Check Morning, Oh Sita")
    
