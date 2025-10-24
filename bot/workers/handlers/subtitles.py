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
from bot.workers.encoders.encode import Encoder


_add_subtitles_sessions = {}


async def add_subtitles(event, args, client):
    """
    Add subtitles to a video.
    Usage: Reply to a video with /sub and then send the subtitle file.
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return

    if event.is_reply and not user_id in _add_subtitles_sessions:
        reply_message = await event.get_reply_message()
        if reply_message.video:
            _add_subtitles_sessions[user_id] = reply_message
            return await event.reply("Please send the subtitle file now.")

    if user_id in _add_subtitles_sessions and event.document:
        video_message = _add_subtitles_sessions.pop(user_id)
        input_file = await event.client.download_media(video_message)
        subtitle_file = await event.client.download_media(event.message)
        output_file = f"subtitled_{os.path.basename(input_file)}"
        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-i",
            subtitle_file,
            "-c",
            "copy",
            "-c:s",
            "mov_text",
            output_file,
        ]

        encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
        await encoder.start(" ".join(cmd))
        await encoder.callback(input_file, output_file, event, user_id)
        stdout, stderr = await encoder.await_completion()

        if stderr:
            await event.reply(f"Error during subtitling: ```{stderr.decode()}```")
        else:
            await event.client.send_file(event.chat_id, output_file)

        os.remove(input_file)
        os.remove(subtitle_file)
        os.remove(output_file)
    else:
        await event.reply("Please reply to a video with /sub first.")


_add_hsub_sessions = {}


async def add_hardcoded_subtitles(event, args, client):
    """
    Add hardcoded subtitles to a video.
    Usage: Reply to a video with /hsub and then send the subtitle file.
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return

    if event.is_reply and not user_id in _add_hsub_sessions:
        reply_message = await event.get_reply_message()
        if reply_message.video:
            _add_hsub_sessions[user_id] = reply_message
            return await event.reply("Please send the subtitle file now.")

    if user_id in _add_hsub_sessions and event.document:
        video_message = _add_hsub_sessions.pop(user_id)
        input_file = await event.client.download_media(video_message)
        subtitle_file = await event.client.download_media(event.message)
        output_file = f"hardcoded_subtitled_{os.path.basename(input_file)}"
        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-vf",
            f"subtitles={subtitle_file}",
            output_file,
        ]

        encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
        await encoder.start(" ".join(cmd))
        await encoder.callback(input_file, output_file, event, user_id)
        stdout, stderr = await encoder.await_completion()

        if stderr:
            await event.reply(f"Error during hardcoding subtitles: ```{stderr.decode()}```")
        else:
            await event.client.send_file(event.chat_id, output_file)

        os.remove(input_file)
        os.remove(subtitle_file)
        os.remove(output_file)
    else:
        await event.reply("Please reply to a video with /hsub first.")


from .handler_utils import handle_video_command


@handle_video_command
async def remove_subtitles(event, args, client, reply_message):
    """
    Remove subtitles from a video.
    Usage: Reply to a video with /rsub
    """
    user_id = event.sender_id
    input_file = await event.client.download_media(reply_message)
    output_file = f"no_subtitles_{os.path.basename(input_file)}"
    cmd = ["ffmpeg", "-i", input_file, "-sn", output_file]

    encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
    await encoder.start(" ".join(cmd))
    await encoder.callback(input_file, output_file, event, user_id)
    stdout, stderr = await encoder.await_completion()

    if stderr:
        await event.reply(f"Error during subtitle removal: ```{stderr.decode()}```")
    else:
        await event.client.send_file(event.chat_id, output_file)

    os.remove(input_file)
    os.remove(output_file)


import os
from bot.utils.ffmpeg_utils import extract_subtitles as extract_sub_func


import asyncio
from bot.utils.ffmpeg_utils import get_subtitle_streams


@handle_video_command
async def extract_subtitles(event, args, client, reply_message):
    """
    Extract subtitles from a video.
    Usage: Reply to a video with /extract_sub
    """
    user_id = event.sender_id
    input_file = await event.client.download_media(reply_message)

    subtitle_streams = await get_subtitle_streams(input_file)
    if not subtitle_streams:
        os.remove(input_file)
        return await event.reply("No subtitles found in this video.")

    for stream in subtitle_streams:
        index = stream["index"]
        output_file = f"subtitle_{index}.srt"
        cmd = ["ffmpeg", "-i", input_file, "-map", f"0:{index}", output_file]

        encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
        await encoder.start(" ".join(cmd))
        await encoder.callback(input_file, output_file, event, user_id)
        stdout, stderr = await encoder.await_completion()

        if stderr:
            await event.reply(f"Error extracting subtitle stream {index}: ```{stderr.decode()}```")
        else:
            await event.client.send_file(event.chat_id, output_file)
            os.remove(output_file)

    os.remove(input_file)
