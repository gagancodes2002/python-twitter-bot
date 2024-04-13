# write code to filter out accounts that are working

import random
import string
from twikit.client import Client


accounts = open('data/store/accounts.txt', 'r')
accounts = accounts.readlines()
accountsList = []
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
    
def check_account(obj):
    try:
        print('Checking account {username}'.format(username=obj['username']))
        # make 6 char alphanumberic random length session_id using obj['username'] as the seed
        session_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        client = Client('en-US',proxy='http://user_3cca1a,type_residential,session_{username}:ironman2002@portal.anyip.io:1080'.format(username=session_id),timeout=None)
        client.set_cookies(
            {
            'auth_token': obj['auth_token'],
            'ct0': obj['token']
            }
        )
        info = client.user()
        # the result will be a dictionary with the user information <User id="1065422520868843520"> return true if the user is valid
        return info.id is not None
    except Exception as e:
        print('Exception : {dikkat}'.format(dikkat=e))
        return False

# status =  check_account(accountsList[57])
# print('Status : {status}'.format(status=status))

# write a code to filter out accounts that are working and save them to a file

# def filter_accounts(accountsList):
#     valid_accounts = []
#     for i in range(len(accountsList)):
#         print('Checking account {i} of {n}'.format(i=i,n=len(accountsList)))
#         if check_account(accountsList[i]):
#             print('Account {i} is valid'.format(i=i))
#             valid_accounts.append(accountsList[i])

# valid_accounts = filter_accounts(accountsList)
# print('Found {n} valid accounts out of {m}'.format(n=len(valid_accounts),m=len(accountsList)))
# # write the valid accounts to a file
# with open('data/store/valid_accounts.txt', 'w') as f:
#     for account in valid_accounts:
#         f.write('{email}:{password}:{username}:{token}:{auth_token}\n'.format(email=account['email'],password=account['password'],username=account['username'],token=account['token'],auth_token=account['auth_token']))

# use threads to speed up the process and filter out the accounts that are working and save them to a file also print the number of valid accounts found and the total number of accounts and print the status of each account as it is being checked

def filterAccountsUsingThreads(accountsList):
    import threading
    valid_accounts = []
    def check_account_and_save(obj):
        if check_account(obj):
            print('Account {username} is valid'.format(username=obj['username']))
            valid_accounts.append(obj)
    threads = []
    for account in accountsList:
        thread = threading.Thread(target=check_account_and_save, args=(account,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print('Found {n} valid accounts out of {m}'.format(n=len(valid_accounts),m=len(accountsList)))
    # write the valid accounts to a file
    with open('data/store/valid_accounts.txt', 'w') as f:
        for account in valid_accounts:
            f.write('{email}:{password}:{username}:{token}:{auth_token}\n'.format(email=account['email'],password=account['password'],username=account['username'],token=account['token'],auth_token=account['auth_token']))
            
filterAccountsUsingThreads(accountsList)

# use asyncio to speed up the process and filter out the accounts that are working and save them to a file also print the number of valid accounts found and the total number of accounts and print the status of each account as it is being checked
    