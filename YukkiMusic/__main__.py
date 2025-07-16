#
# Copyright (C) 2021-2022 by TeamYukki@Github
#

import asyncio
import importlib
import sys
import time
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from YukkiMusic import LOGGER, app, userbot
from YukkiMusic.core.call import Yukki
from YukkiMusic.plugins import ALL_MODULES
from YukkiMusic.utils.database import get_banned_users, get_gbanned

loop = asyncio.get_event_loop()

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("YukkiMusic").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return

    if (
        not config.SPOTIFY_CLIENT_ID
        and not config.SPOTIFY_CLIENT_SECRET
    ):
        LOGGER("YukkiMusic").warning(
            "No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )

    # 🔧 Time sync workaround for Pyrogram 1.4.16
    LOGGER("YukkiMusic").info("Waiting 10 seconds for system time to stabilize...")
    time.sleep(10)

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    # 🔁 Try starting Pyrogram, retry if msg_id is too low
    try:
        await app.start()
    except Exception as e:
        LOGGER("YukkiMusic").warning(f"Pyrogram failed to start: {e}")
        LOGGER("YukkiMusic").info("Retrying app.start() after 5 seconds...")
        await asyncio.sleep(5)
        await app.start()

    for all_module in ALL_MODULES:
        importlib.import_module("YukkiMusic.plugins" + all_module)
    LOGGER("Yukkimusic.plugins").info("Successfully Imported Modules")

    await userbot.start()
    await Yukki.start()

    try:
        await Yukki.stream_call(
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )
    except NoActiveGroupCall:
        LOGGER("YukkiMusic").error(
            "[ERROR] - \n\nPlease turn on your Logger Group's Voice Call. Make sure you never close/end voice call in your log group"
        )
        sys.exit()
    except:
        pass

    await Yukki.decorators()
    LOGGER("YukkiMusic").info("Yukki Music Bot Started Successfully")
    await idle()

if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("YukkiMusic").info("Stopping Yukki Music Bot! GoodBye")
