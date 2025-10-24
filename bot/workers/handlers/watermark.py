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

import os
from bot.utils.msg_utils import user_is_allowed
from bot.utils.os_utils import s_remove


async def set_watermark(event, args, client):
    """
    Set a custom watermark for a video.
    Usage: Reply to a message with a photo to set the watermark.
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return
    if not event.is_reply:
        return await event.reply("Please reply to a message with a photo to set the watermark.")
    reply_message = await event.get_reply_message()
    if not reply_message.photo:
        return await event.reply("Please reply to a message with a photo to set the watermark.")

    watermark_file = "watermark.png"
    s_remove(watermark_file)
    await event.client.download_media(reply_message.media, file=watermark_file)
    await event.reply("**Watermark Saved Successfully.**")


from bot.utils.os_utils import file_exists


async def get_watermark(event, args, client):
    """
    Get the current watermark.
    Usage: /getwatermark
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return
    watermark_file = "watermark.png"
    if not file_exists(watermark_file):
        return await event.reply("No watermark found.")
    await event.reply(file=watermark_file)


from bot.workers.encoders.encode import Encoder


async def add_watermark(event, args, client):
    """
    Add a watermark to a video.
    Usage: Reply to a video with /addwatermark
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return
    if not event.is_reply:
        return await event.reply("Please reply to a video to add a watermark.")
    reply_message = await event.get_reply_message()
    if not reply_message.video:
        return await event.reply("Please reply to a video to add a watermark.")
    if not file_exists("watermark.png"):
        return await event.reply("Please set a watermark first using /setwatermark.")

    input_file = await event.client.download_media(reply_message)
    output_file = f"watermarked_{os.path.basename(input_file)}"
    cmd = f"ffmpeg -i '{input_file}' -i watermark.png -filter_complex '[0:v][1:v]overlay=10:10' '{output_file}'"

    encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
    await encoder.start(cmd)
    await encoder.callback(input_file, output_file, event, user_id)
    stdout, stderr = await encoder.await_completion()

    if stderr:
        await event.reply(f"Error during watermarking: ```{stderr.decode()}```")
    else:
        await event.client.send_file(event.chat_id, output_file)

    os.remove(input_file)
    os.remove(output_file)

async def spoiler(event, args, client):
    """
    Add a spoiler to a video.
    Usage: Reply to a video with /spoiler
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return
    if not event.is_reply:
        return await event.reply("Please reply to a video to add a spoiler.")
    reply_message = await event.get_reply_message()
    if not reply_message.video:
        return await event.reply("Please reply to a video to add a spoiler.")

    input_file = await event.client.download_media(reply_message)
    output_file = f"spoiler_{os.path.basename(input_file)}"
    cmd = f"ffmpeg -i '{input_file}' -vf 'boxblur=10' '{output_file}'"

    encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
    await encoder.start(cmd)
    await encoder.callback(input_file, output_file, event, user_id)
    stdout, stderr = await encoder.await_completion()

    if stderr:
        await event.reply(f"Error during spoiler effect: ```{stderr.decode()}```")
    else:
        await event.client.send_file(event.chat_id, output_file)

    os.remove(input_file)
    os.remove(output_file)
