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

from bot.utils.msg_utils import user_is_allowed, user_is_owner
from bot.workers.encoders.encode import Encoder
from bot.utils.ffmpeg_utils import get_media_info as get_media_info_func
from bot.config import conf
import os


async def set_media_type(event, args, client):
    """
    Set the media type of a file.
    Usage: Reply to a file with /setmedia <media_type>
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return
    if not event.is_reply:
        return await event.reply("Please reply to a file to set its media type.")
    reply_message = await event.get_reply_message()
    if not (reply_message.video or reply_message.document):
        return await event.reply("Please reply to a video or document.")
    if not args:
        return await event.reply(
            "Please provide a media type. (e.g., /setmedia document)"
        )
    media_type = args.lower()
    if media_type not in ["video", "document", "audio"]:
        return await event.reply("Invalid media type. Please choose from: video, document, audio.")

    input_file = await event.client.download_media(reply_message)

    await event.client.send_file(event.chat_id, input_file, force_document=(media_type == "document"))

    os.remove(input_file)


async def upload_file(event, args, client):
    """
    Upload a file.
    Usage: /upload <file_name>
    """
    user_id = event.sender_id
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply("Please provide a file name to upload.")

    safe_dir = conf.SAFE_UPLOAD_DIR
    file_path = os.path.join(safe_dir, args)

    if not os.path.abspath(file_path).startswith(os.path.abspath(safe_dir)):
        return await event.reply("Invalid file path.")

    if not os.path.exists(file_path):
        return await event.reply("File not found.")

    await event.client.send_file(event.chat_id, file_path)


from bot.workers.encoders.encode import Encoder


from bot.utils.ffmpeg_utils import get_media_info as get_media_info_func


async def get_media_info(event, args, client):
    """
    Get media info of a file.
    Usage: Reply to a file with /mediainfo
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return
    if not event.is_reply:
        return await event.reply("Please reply to a file to get its media info.")
    reply_message = await event.get_reply_message()
    if not (reply_message.video or reply_message.document):
        return await event.reply("Please reply to a video or document.")

    input_file = await event.client.download_media(reply_message)
    media_info = await get_media_info_func(input_file)
    os.remove(input_file)

    if media_info:
        await event.reply(f"```\n{media_info}\n```")
    else:
        await event.reply("Failed to get media info.")
