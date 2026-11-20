from pyrogram import Client

import config

from ..logging import LOGGER

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="PROAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistants...")
        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("ProBotGc")
                await self.one.join_chat("ProBotts")
            except:
                pass
            assistants.append(1)
            try:
                await self.one.send_message(config.LOGGER_ID, "Assistant Started")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 1 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                exit()
            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Assistant Started as {self.one.name}")


    async def stop(self):
        LOGGER(__name__).info(f"Stopping Assistants...")
        try:
            if config.STRING1:
                await self.one.stop()
        except:
            pass
