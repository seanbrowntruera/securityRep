import json
import os

from slack_sdk import WebClient

USERAUTHTOKEN = os.environ["UserOAuthToken"]
BOTUSERTOKEN = os.environ["BotUserOAuthToken"]

client = WebClient(token=BOTUSERTOKEN)
users_store = {}
users = []
user_names = []


# Put users into the dict
def save_users(users_array):
    for user in users_array:
        # Key user info on their unique user ID
        user_id = user["id"]
        users.append(user_id)

        user_names.append(user["name"])
        # Store the entire user object (you may not need all of the info)
        users_store[user_id] = user


result = client.users_list()
save_users(result["members"])
print(user_names)


def ping_user(name):
    for user in users:
        test = client.chat_postMessage(channel=user,
                                       text="hello this is a test")

        print(test)