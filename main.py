import json
import random
from src.instadm import InstaDM
from selenium.common.exceptions import NoSuchElementException


with open('infos/accounts.json', 'r') as f:
    accounts = json.load(f)

with open('infos/usernames.txt', 'r') as f:
    usernames = [line.strip() for line in f]

with open('infos/messages.txt', 'r') as f:
    messages = [line.strip() for line in f]
    
    


while True:
    if not usernames:
        print('Finished usernames.')
        break

    dm_num = int(input('How many DM you want to send in each account: '))

    for account in accounts:
        if not usernames:
            break
            # Auto login
        insta = InstaDM(
            username=account["username"], password=account["password"], headless=False)

        for i in range(dm_num):
            username = usernames.pop()
            # Send message
            try:
                success = insta.sendMessage(
                    user=username, message=random.choice(messages))
                if not success:
                    insta.teardown()
                continue
            except NoSuchElementException:
                # User not found = move on to the next user
                continue
            except Exception as e:
                if "timed out. Element not found with XPATH : //textarea[@placeholder]" in str(e):
                    insta.teardown()
                continue
            # other error occured = move on to the next user
        # Log out
        insta.teardown()
