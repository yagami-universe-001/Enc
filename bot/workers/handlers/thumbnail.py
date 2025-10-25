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

from bot.utils.msg_utils import user_is_allowed


from bot import thumb
from bot.utils.os_utils import s_remove


from bot.utils.bot_utils import get_var
from bot.utils.msg_utils import msg_sleep_delete


async def set_thumbnail(event, args, client):
    """
    Set a custom thumbnail for a video.
    Usage: Reply to a video with /setthumb and send an image.
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return
    if not event.is_reply:
        return await event.reply("Please reply to a message with a photo to set the thumbnail.")
    if not event.is_private and not get_var("groupenc"):
        rply = (
            "`Ignoring…`\nTurn on encoding videos in groups with "
            "`/groupenc on` to enable setting thumbnails in groups.\n"
            "__This message shall self-destruct in 20 seconds.__"
        )
        return await msg_sleep_delete(event, rply, time=20)
    reply_message = await event.get_reply_message()
    if not reply_message.photo:
        return await event.reply("Please reply to a message with a photo to set the thumbnail.")

    s_remove(thumb)
    await event.client.download_media(reply_message.media, file=thumb)
    await event.reply("**Thumbnail Saved Successfully.**")


from bot.utils.os_utils import file_exists


async def get_thumbnail(event, args, client):
    """
    Get the current thumbnail of a video.
    Usage: /getthumb
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return
    if not file_exists(thumb):
        return await event.reply("No thumbnail found.")
    await event.reply(file=thumb)


async def delete_thumbnail(event, args, client):
    """
    Delete the custom thumbnail of a video.
    Usage: /delthumb
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return
    if not file_exists(thumb):
        return await event.reply("No thumbnail found to delete.")
    s_remove(thumb)
    await event.reply("Thumbnail deleted successfully.")

import os
from bot.utils.bot_utils import run_sync_in_thread
from bot.utils.ffmpeg_utils import extract_thumbnail as extract_thumb_func


async def extract_thumbnail(event, args, client):
    """
    Extract the thumbnail from a video.
    Usage: Reply to a video with /extract_thumb
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return
    if not event.is_reply:
        return await event.reply("Please reply to a video to extract its thumbnail.")
    reply_message = await event.get_reply_message()
    if not reply_message.video:
        return await event.reply("Please reply to a video to extract its thumbnail.")

    input_file = await event.client.download_media(reply_message)
    output_file = f"thumbnail_{os.path.basename(input_file)}.jpg"
    thumbnail = await extract_thumb_func(input_file, output_file)
    os.remove(input_file)
    if thumbnail:
        await event.reply(file=thumbnail)
        os.remove(thumbnail)
    else:
        await event.reply("Failed to extract thumbnail.")
