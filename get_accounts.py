# C:\Users\gagan\Downloads\Twitter Sample Sessions\Twitter Sample Sessions

# text file contains 
#.twitter.com	FALSE	/	FALSE	13383517433810014	guest_id_marketing	v1%3A170432452896936975
#.twitter.com	FALSE	/	FALSE	13383517433809944	guest_id_ads	v1%3A170432452896936975
#.twitter.com	FALSE	/	FALSE	13383358026765706	guest_id	v1%3A170432452896936975
#.twitter.com	FALSE	/	FALSE	13383359281494830	kdt	9HqpdNISByyl3PbPSFDwak6haXJgI5kV3m8O4vB3
#.twitter.com	FALSE	/	FALSE	13383517431844345	_ga	GA1.2.999136943.1704324428
#.twitter.com	FALSE	/	FALSE	13383359281494926	auth_token	77acd913941a802e0e48e1ee8c1bea7862468652
#.twitter.com	FALSE	/	FALSE	13383359281606589	ct0	097f248513d86dbaad8ff2bf200a17ee9dfa15b9d182697ea6a068404b7823face6c96a8bc7fd5fe2005d85b7772095356d02790c3a5b326954cc237e0ac4f2c07d22150fa62d6e5d81fe1d4983b0d8a
#.twitter.com	FALSE	/	FALSE	13380493433810063	twid	u%3D1226362470312423426
#.twitter.com	FALSE	/	FALSE	13383517433810046	personalization_id	"v1_qBcWfUCJC/1ya/ouMMCUVg=="


# import all text files in the top directory and save the content in a file called all_accounts.txt in the below manner the original content is in the above manner
# KaykyGodinho:9626599357:kaykyscoob@gmail.com:d448aca5fb34dfa2398da3ef4c3c3a38fed37cc561884315410efd63ed7a6162bb28c900004eb73fc49f0282f6f08623b7db8c54197674ab4a4323e880072db779c09ccc2931eb23b946476e5349a6c4:967e755d94dcc1dcb9845992d4621f3ec98c7c82
# <username>:<password>:<email>:<token>:<auth_token>
# the username will be "null" for our case
# the password will be "null" for our case
# the email will be "null" for our case
# the token will be ct0 for our case
# the auth_token will be auth_token for our case

import os

def get_accounts():
    # get all the text files in the top directory
    # Directory C:\Users\gagan\Downloads\Twitter Sample Sessions\Twitter Sample Sessions
    path = r'C:\Users\gagan\OneDrive\Documents\Personal\python-twitter-bot\data\text_files'
    # fix the path to be used in the os.listdir
    os.chdir(path)
    
    files = [f for f in os.listdir(path) if f.endswith('.txt')]
    with open('all_accounts.txt', 'w') as f:
        for file in files:
            with open(file, 'r') as file:
                auth_token = ""
                ct0 = ""
                for line in file:
                    print(line)
                    parts = line.split("\t")
                    cookie_name = parts[5]
                    cookie_value = parts[6]
                    print(f"{cookie_name}:{cookie_value}")
                    
                    if cookie_name == "auth_token":
                        auth_token = cookie_value.strip()
                    if cookie_name == "ct0":
                        ct0 = cookie_value.strip()
                    if auth_token and ct0:
                        f.write(f"null:null:null:{ct0}:{auth_token}\n")
                        auth_token = ""
                        ct0 = ""
                    # parts = line.split("\t")
                    # username = "null"
                    # password = "null"
                    # email = "null"
                    # token = parts[3]
                    # auth_token = parts[4]
                    # f.write(f"{username}:{password}:{email}:{token}:{auth_token}")
                    # f.write("\n")

get_accounts()