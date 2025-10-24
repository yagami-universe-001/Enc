#    This file is part of the Encoder distribution.
#    Copyright (c) 2023 Danish_00, Nubuki-all
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS for a PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in
# <https://github.com/Nubuki-all/Enc/blob/main/License> .

from bot.config import conf
from bot.utils.msg_utils import user_is_owner
from bot.config_manager import save_config


async def set_shortner(event, args, client):
    """
    Set the shortner.
    Usage: /shortner <shortner>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply(f"Current shortner: `{conf.SHORTNER}`")
    conf.SHORTNER = args
    save_config()
    await event.reply(f"Shortner set to `{args}`.")


async def set_shortlink1(event, args, client):
    """
    Set the shortlink1.
    Usage: /shortlink1 <shortlink1>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply(f"Current shortlink1: `{conf.SHORTLINK1}`")
    conf.SHORTLINK1 = args
    save_config()
    await event.reply(f"Shortlink1 set to `{args}`.")


async def set_shortlink2(event, args, client):
    """
    Set the shortlink2.
    Usage: /shortlink2 <shortlink2>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply(f"Current shortlink2: `{conf.SHORTLINK2}`")
    conf.SHORTLINK2 = args
    save_config()
    await event.reply(f"Shortlink2 set to `{args}`.")


async def set_tutorial1(event, args, client):
    """
    Set the tutorial1.
    Usage: /tutorial1 <tutorial1>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply(f"Current tutorial1: `{conf.TUTORIAL1}`")
    conf.TUTORIAL1 = args
    save_config()
    await event.reply(f"Tutorial1 set to `{args}`.")
