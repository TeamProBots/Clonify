import time
import random
from datetime import datetime

import psutil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Clonify import app
from config import PING_IMG_URL, STREAMI_PICS
from .utils import StartTime
from Clonify.utils import get_readable_time
from Clonify.utils.decorators.language import language

APP_LINK = f"https://t.me/AqiaBot"


@Client.on_message(filters.command("clone"))
@language
async def ping_clone(client: Client, message: Message, _):
    bot = await client.get_me()


    hmm = await message.reply_photo(
        photo=random.choice(STREAMI_PICS), caption=_["NO_CLONE_MSG"],
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Cʟᴏɴᴇ Bᴏᴛ", url=APP_LINK)]
            ]
        )
    )
