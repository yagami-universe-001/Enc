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
from .handler_utils import handle_video_command
from bot.workers.encoders.encode import Encoder


@handle_video_command
async def extract_audio(event, args, client, reply_message):
    """
    Extract audio from a video.
    Usage: Reply to a video with /extract_audio
    """
    user_id = event.sender_id
    input_file = await event.client.download_media(reply_message)
    output_file = f"audio_{os.path.basename(input_file)}.m4a"
    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-vn",
        "-acodec",
        "copy",
        output_file,
    ]

    encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
    await encoder.start(*cmd)
    await encoder.callback(input_file, output_file, event, user_id)
    stdout, stderr = await encoder.await_completion()

    if stderr:
        await event.reply(f"Error during audio extraction: ```{stderr.decode()}```")
    else:
        await event.client.send_file(event.chat_id, output_file)

    os.remove(input_file)
    os.remove(output_file)




_add_audio_sessions = {}


async def add_audio(event, args, client):
    """
    Add audio to a video.
    Usage: Reply to a video with /addaudio and then send the audio file.
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return

    if event.is_reply and not user_id in _add_audio_sessions:
        reply_message = await event.get_reply_message()
        if reply_message.video:
            _add_audio_sessions[user_id] = reply_message
            return await event.reply("Please send the audio file now.")

    if user_id in _add_audio_sessions and event.audio:
        video_message = _add_audio_sessions.pop(user_id)
        input_file = await event.client.download_media(video_message)
        audio_file = await event.client.download_media(event.message)
        output_file = f"audio_added_{os.path.basename(input_file)}"
        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-i",
            audio_file,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            output_file,
        ]

        encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
        await encoder.start(*cmd)
        await encoder.callback(input_file, output_file, event, user_id)
        stdout, stderr = await encoder.await_completion()

        if stderr:
            await event.reply(f"Error during audio addition: ```{stderr.decode()}```")
        else:
            await event.client.send_file(event.chat_id, output_file)

        os.remove(input_file)
        os.remove(audio_file)
        os.remove(output_file)
    else:
        await event.reply("Please reply to a video with /addaudio first.")


@handle_video_command
async def remove_audio(event, args, client, reply_message):
    """
    Remove audio from a video.
    Usage: Reply to a video with /remaudio
    """
    user_id = event.sender_id
    input_file = await event.client.download_media(reply_message)
    output_file = f"no_audio_{os.path.basename(input_file)}"
    cmd = ["ffmpeg", "-i", input_file, "-an", output_file]

    encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
    await encoder.start(*cmd)
    await encoder.callback(input_file, output_file, event, user_id)
    stdout, stderr = await encoder.await_completion()

    if stderr:
        await event.reply(f"Error during audio removal: ```{stderr.decode()}```")
    else:
        await event.client.send_file(event.chat_id, output_file)

    os.remove(input_file)
    os.remove(output_file)
