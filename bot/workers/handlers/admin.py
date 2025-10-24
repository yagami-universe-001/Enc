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

from bot.utils.msg_utils import user_is_owner


from bot.workers.handlers.manage import restart


async def restart_bot(event, args, client):
    """
    Restart the bot.
    Usage: /restart
    """
    user_id = event.sender_id
    if not user_is_owner(user_id):
        return await event.reply("You are not authorized to use this command.")
    await restart(event, args, client)


from bot.workers.handlers.queue import listqueue


async def view_queue(event, args, client):
    """
    View the encoding queue.
    Usage: /queue
    """
    user_id = event.sender_id
    if not user_is_owner(user_id):
        return await event.reply("You are not authorized to use this command.")
    await listqueue(event, args, client)


from bot.workers.handlers.queue import clearqueue


async def clear_queue(event, args, client):
    """
    Clear the encoding queue.
    Usage: /clear
    """
    user_id = event.sender_id
    if not user_is_owner(user_id):
        return await event.reply("You are not authorized to use this command.")
    await clearqueue(event, args, client)
