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


async def add_channel(event, args, client):
    """
    Add a channel to the list of allowed channels.
    Usage: /addchnl <channel_id>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply("Please provide a channel ID.")
    conf.ALLOWED_CHANNELS.append(int(args))
    save_config()
    await event.reply(f"Channel `{args}` added to the list of allowed channels.")


async def list_channels(event, args, client):
    """
    List the allowed channels.
    Usage: /listchnl
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    await event.reply(f"Allowed channels: `{conf.ALLOWED_CHANNELS}`")


async def add_paid_user(event, args, client):
    """
    Add a user to the list of paid users.
    Usage: /addpaid <user_id>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply("Please provide a user ID.")
    conf.PAID_USERS.append(int(args))
    save_config()
    await event.reply(f"User `{args}` added to the list of paid users.")


async def list_paid_users(event, args, client):
    """
    List the paid users.
    Usage: /listpaid
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    await event.reply(f"Paid users: `{conf.PAID_USERS}`")


async def delete_channel(event, args, client):
    """
    Delete a channel from the list of allowed channels.
    Usage: /delchnl <channel_id>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply("Please provide a channel ID.")
    try:
        conf.ALLOWED_CHANNELS.remove(int(args))
        save_config()
        await event.reply(f"Channel `{args}` removed from the list of allowed channels.")
    except ValueError:
        await event.reply(f"Channel `{args}` not found in the list of allowed channels.")


async def fsub_mode(event, args, client):
    """
    Set the fsub mode.
    Usage: /fsub_mode <mode>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply(f"Current fsub mode: `{conf.FSUB_MODE}`")
    conf.FSUB_MODE = args
    save_config()
    await event.reply(f"Fsub mode set to `{args}`.")


async def remove_paid_user(event, args, client):
    """
    Remove a user from the list of paid users.
    Usage: /rempaid <user_id>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply("Please provide a user ID.")
    try:
        conf.PAID_USERS.remove(int(args))
        save_config()
        await event.reply(f"User `{args}` removed from the list of paid users.")
    except ValueError:
        await event.reply(f"User `{args}` not found in the list of paid users.")


from bot.utils.os_utils import updater


async def update_bot(event, args, client):
    """
    Update the bot.
    Usage: /update
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")

    reply = await event.reply("`Updating...`")
    await updater(reply)
