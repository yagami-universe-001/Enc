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

from functools import wraps
from bot.utils.msg_utils import user_is_allowed


def handle_video_command(func):
    @wraps(func)
    async def wrapper(event, args, client):
        user_id = event.sender_id
        if not user_is_allowed(user_id):
            return

        if not event.is_reply:
            return await event.reply("Please reply to a video.")
        reply_message = await event.get_reply_message()
        if not reply_message.video:
            return await event.reply("Please reply to a video.")

        await func(event, args, client, reply_message)

    return wrapper
