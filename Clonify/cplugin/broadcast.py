import asyncio

from pyrogram import filters, Client
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait

from Clonify import app
from Clonify.misc import SUDOERS
from Clonify.utils.database import (
    get_client,
    get_served_chats_clone,
    get_served_users_clone,
)
from Clonify.utils.decorators.language import language
from Clonify.utils.formatters import alpha_to_int
from config import adminlist
import random
from typing import Dict, List, Union

from Clonify import userbot
from Clonify.core.mongo import mongodb, pymongodb
from Clonify.utils.database.clonedb import get_owner_id_from_db, check_bot_premium
from config import SUPPORT_CHAT, OWNER_ID

authdb = mongodb.adminauth
authuserdb = mongodb.authuser
autoenddb = mongodb.autoend
assdb = mongodb.assistants
blacklist_chatdb = mongodb.blacklistChat
blockeddb = mongodb.blockedusers
chatsdbc = mongodb.chatsc
channeldb = mongodb.cplaymode
clonebotdb = pymongodb.clonebotdb
countdb = mongodb.upcount
gbansdb = mongodb.gban
langdb = mongodb.language
onoffdb = mongodb.onoffper
playmodedb = mongodb.playmode
playtypedb = mongodb.playtypedb
skipdb = mongodb.skipmode
sudoersdb = mongodb.sudoers
usersdbc = mongodb.tgusersdbc
privatedb = mongodb.privatechats
suggdb = mongodb.suggestion
cleandb = mongodb.cleanmode
queriesdb = mongodb.queries
userdb = mongodb.userstats
videodb = mongodb.vipvideocalls

# Shifting to memory [mongo sucks often]
active = []
activevideo = []
assistantdict = {}
autoend = {}
count = {}
channelconnect = {}
langm = {}
loop = {}
maintenance = []
nonadmin = {}
pause = {}
playmode = {}
playtype = {}
skipmode = {}
privatechats = {}
cleanmode = []
suggestion = {}
mute = {}
audio = {}
video = {}


async def get_active_chats_clone() -> list:
    return active


async def is_active_chat_clone(chat_id: int) -> bool:
    if chat_id not in active:
        return False
    else:
        return True


async def add_active_chat_clone(chat_id: int):
    if chat_id not in active:
        active.append(chat_id)


async def remove_active_chat_clone(chat_id: int):
    if chat_id in active:
        active.remove(chat_id)


async def _get_authusers(chat_id: int) -> Dict[str, int]:
    _notes = await authuserdb.find_one({"chat_id": chat_id})
    if not _notes:
        return {}
    return _notes["notes"]


async def get_authuser_names_clone(chat_id: int) -> List[str]:
    _notes = []
    for note in await _get_authusers(chat_id):
        _notes.append(note)
    return _notes


async def get_authuser_clone(chat_id: int, name: str) -> Union[bool, dict]:
    name = name
    _notes = await _get_authusers(chat_id)
    if name in _notes:
        return _notes[name]
    else:
        return False


async def save_authuser_clone(chat_id: int, name: str, note: dict):
    name = name
    _notes = await _get_authusers(chat_id)
    _notes[name] = note

    await authuserdb.update_one(
        {"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True
    )


async def delete_authuser_clone(chat_id: int, name: str) -> bool:
    notesd = await _get_authusers(chat_id)
    name = name
    if name in notesd:
        del notesd[name]
        await authuserdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"notes": notesd}},
            upsert=True,
        )
        return True
    return False

# Broadcast command
IS_BROADCASTING = False


@Client.on_message(filters.command(["broadcast"]))
@language
async def broadcast_message(client, message, _):

    # Get bot ID
    bot = await client.get_me()
    bot_id = bot.id

    # get owner info
    C_OWNER = get_owner_id_from_db(bot_id)
    OWNERS = [OWNER_ID, C_OWNER]

    if message.from_user.id not in OWNERS:
        return await message.reply_text(_["c_brod_1"].format(SUPPORT_CHAT))

    global IS_BROADCASTING

    # Check if bot has premium
    a = await client.get_me()
    premium_status = check_bot_premium(a.id)
    if premium_status is None:
        return await message.reply_text("Bot ID not found!")
    elif not premium_status:
        if message.from_user.id != OWNER_ID:
            return await message.reply_text("Premium not found!")
        else:
            pass

    # Get the message content
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            IS_BROADCASTING = False
            return await message.reply_text(_["broad_2"])
        query = message.text.split(None, 1)[1]
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if query == "":
            IS_BROADCASTING = False
            return await message.reply_text(_["broad_8"])
        
    # Start broadcasting
    IS_BROADCASTING = True
    await message.reply_text(_["broad_1"])

    # Broadcast to chats
    if "-nobot" not in message.text:
        sent, pin = 0, 0
        served_chats = await get_served_chats_clone(bot_id)
        for chat in served_chats:
            try:
                chat_id = int(chat["chat_id"])
                m = (
                    await client.forward_messages(chat_id, y, x)
                    if message.reply_to_message
                    else await client.send_message(chat_id, text=query)
                )
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except:
                        pass
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except:
                        pass
                sent += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except:
                continue

        try:
            await message.reply_text(_["broad_3"].format(sent, pin))
        except:
            pass

    # Broadcast to users
    if "-user" in message.text:
        susr = 0
        served_users = await get_served_users_clone(bot_id)
        for user in served_users:
            try:
                user_id = int(user["user_id"])
                m = (
                    await client.forward_messages(user_id, y, x)
                    if message.reply_to_message
                    else await client.send_message(user_id, text=query)
                )
                susr += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except:
                pass

        try:
            await message.reply_text(_["broad_4"].format(susr))
        except:
            pass

# Zeo

    IS_BROADCASTING = False
