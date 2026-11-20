from Clonify.core.mongo import mongodb, pymongodb
from typing import Dict, List, Union

cloneownerdb = mongodb.cloneownerdb
clonebotdb = pymongodb.clonebotdb
clonebotnamedb = mongodb.clonebotnamedb


# clone bot owner
async def save_clonebot_owner(bot_id, user_id):
    await cloneownerdb.insert_one({"bot_id": bot_id, "user_id": user_id})


async def get_clonebot_owner(bot_id):
    result = await cloneownerdb.find_one({"bot_id": bot_id})
    if result:
        return result.get("user_id")
    else:
        return False


async def save_clonebot_username(bot_id, user_name):
    await clonebotnamedb.insert_one({"bot_id": bot_id, "user_name": user_name})


async def get_clonebot_username(bot_id):
    result = await clonebotnamedb.find_one({"bot_id": bot_id})
    if result:
        return result.get("user_name")
    else:
        return False


# new clone 

# Function to get owner_id dynamically for a given bot_id
def get_owner_id_from_db(bot_id):
    # MongoDB query to find the bot data using bot_id
    bot_data = clonebotdb.find_one({"bot_id": bot_id})
    if bot_data:
        return bot_data["user_id"]  # Assuming 'user_id' is the owner of the bot
    return None  # If no bot is found, return None

#check premium -------------
def check_bot_premium(bot_id):
    bot_details = clonebotdb.find_one({"bot_id": bot_id})

    if bot_details:
        if bot_details["premium"]:
            return True 
        else:
            return False
    else:
        return None
#check premium --------------

"""
# Function to get Support Chats dynamically for a given bot_id
def get_cloned_support_chat(bot_id):
    # MongoDB query to find the bot data using bot_id
    bot_data = clonebotdb.find_one({"bot_id": bot_id})
    if bot_data:
        return bot_data["support"]
    return None

# Function to get Support Channel dynamically for a given bot_id
def get_cloned_support_channel(bot_id):
    # MongoDB query to find the bot data using bot_id
    bot_data = clonebotdb.find_one({"bot_id": bot_id})
    if bot_data:
        return bot_data["channel"]
    return None
"""

async def get_cloned_support_chat(bot_id: int) -> str:
    bot_details = clonebotdb.find_one({"bot_id": bot_id})
    return bot_details.get("support", "No support chat set.")

async def get_cloned_support_channel(bot_id: int) -> str:
    bot_details = clonebotdb.find_one({"bot_id": bot_id})
    return bot_details.get("channel", "No channel set.")


async def has_user_cloned_any_bot(user_id: int) -> bool:
    # Check if the user has cloned any bot (search by user_id)
    cloned_bot = clonebotdb.find_one({"user_id": user_id})
    
    if cloned_bot:
        return True
    
    return False
