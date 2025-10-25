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


import os
from bot.workers.encoders.encode import Encoder


from .handler_utils import handle_video_command

@handle_video_command
async def _encode_resolution(event, client, resolution, reply_message, input_file=None, delete_input=True):
    user_id = event.sender_id
    if not input_file:
        input_file = await event.client.download_media(reply_message)

    output_file = f"{resolution}_{os.path.basename(input_file)}"
    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-vf",
        f"scale=-2:{resolution.replace('p', '')}",
        output_file,
    ]

    encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
    await encoder.start(*cmd)
    await encoder.callback(input_file, output_file, event, user_id)
    stdout, stderr = await encoder.await_completion()

    if stderr:
        await event.reply(f"Error during {resolution} encoding: ```{stderr.decode()}```")
    else:
        await event.client.send_file(event.chat_id, output_file)

    if delete_input:
        os.remove(input_file)
    os.remove(output_file)


async def encode_144p(event, args, client):
    await _encode_resolution(event, client, "144p")


async def encode_240p(event, args, client):
    await _encode_resolution(event, client, "240p")


async def encode_360p(event, args, client):
    await _encode_resolution(event, client, "360p")


async def encode_480p(event, args, client):
    await _encode_resolution(event, client, "480p")


async def encode_720p(event, args, client):
    await _encode_resolution(event, client, "720p")


async def encode_1080p(event, args, client):
    await _encode_resolution(event, client, "1080p")


async def encode_2160p(event, args, client):
    await _encode_resolution(event, client, "2160p")


async def encode_all(event, args, client):
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return
    if not event.is_reply:
        return await event.reply("Please reply to a video to encode it in all resolutions.")
    reply_message = await event.get_reply_message()
    if not reply_message.video:
        return await event.reply("Please reply to a video to encode it in all resolutions.")

    input_file = await event.client.download_media(reply_message)
    resolutions = ["144p", "240p", "360p", "480p", "720p", "1080p", "2160p"]
    for i, resolution in enumerate(resolutions):
        delete_input = (i == len(resolutions) - 1)
        await _encode_resolution(event, client, resolution, input_file, delete_input)
