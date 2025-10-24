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


from bot.utils.bot_utils import run_sync_in_thread
from bot.utils.ffmpeg_utils import get_video_streams
from .handler_utils import handle_video_command
from bot.workers.encoders.encode import Encoder


@handle_video_command
async def compress_video(event, args, client, reply_message):
    """
    Compress a video.
    Usage: Reply to a video with /compress
    """
    user_id = event.sender_id
    input_file = await event.client.download_media(reply_message)
    output_file = f"compressed_{os.path.basename(input_file)}"
    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-c:v",
        "libx265",
        "-crf",
        "28",
        output_file,
    ]

    encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
    await encoder.start(" ".join(cmd))
    await encoder.callback(input_file, output_file, event, user_id)
    stdout, stderr = await encoder.await_completion()

    if stderr:
        await event.reply(f"Error during compression: ```{stderr.decode()}```")
    else:
        await event.client.send_file(event.chat_id, output_file)

    os.remove(input_file)
    os.remove(output_file)


@handle_video_command
async def cut_video(event, args, client, reply_message):
    """
    Cut a video.
    Usage: Reply to a video with /cut <start> <end>
    """
    user_id = event.sender_id
    if not args:
        return await event.reply(
            "Please provide start and end times for cutting the video. (e.g., /cut 00:00:10 00:00:20)"
        )
    try:
        start_time, end_time = args.split()
    except ValueError:
        return await event.reply(
            "Invalid format. Please provide start and end times. (e.g., /cut 00:00:10 00:00:20)"
        )

    input_file = await event.client.download_media(reply_message)
    output_file = f"cut_{os.path.basename(input_file)}"
    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-c",
        "copy",
        output_file,
    ]

    encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
    await encoder.start(" ".join(cmd))
    await encoder.callback(input_file, output_file, event, user_id)
    stdout, stderr = await encoder.await_completion()

    if stderr:
        await event.reply(f"Error during cutting: ```{stderr.decode()}```")
    else:
        await event.client.send_file(event.chat_id, output_file)

    os.remove(input_file)
    os.remove(output_file)

@handle_video_command
async def crop_video(event, args, client, reply_message):
    """
    Crop a video.
    Usage: Reply to a video with /crop <width:height:x:y>
    """
    user_id = event.sender_id
    if not args:
        return await event.reply(
            "Please provide crop dimensions. (e.g., /crop 1280:720:0:0)"
        )
    try:
        width, height, x, y = args.split(":")
    except ValueError:
        return await event.reply(
            "Invalid format. Please provide crop dimensions. (e.g., /crop 1280:720:0:0)"
        )

    input_file = await event.client.download_media(reply_message)
    output_file = f"cropped_{os.path.basename(input_file)}"
    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-vf",
        f"crop={width}:{height}:{x}:{y}",
        output_file,
    ]

    encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
    await encoder.start(" ".join(cmd))
    await encoder.callback(input_file, output_file, event, user_id)
    stdout, stderr = await encoder.await_completion()

    if stderr:
        await event.reply(f"Error during cropping: ```{stderr.decode()}```")
    else:
        await event.client.send_file(event.chat_id, output_file)

    os.remove(input_file)
    os.remove(output_file)

_merging_sessions = {}


@handle_video_command
async def rename_video(event, args, client, reply_message):
    """
    Rename a video.
    Usage: Reply to a video with /rename <new_name>
    """
    user_id = event.sender_id
    if not args:
        return await event.reply("Please provide a new name for the video.")

    input_file = await event.client.download_media(reply_message)

    # Sanitize the new name to prevent path traversal
    new_name = os.path.basename(args)
    output_file = f"{new_name}{os.path.splitext(input_file)[1]}"

    os.rename(input_file, output_file)

    await event.client.send_file(event.chat_id, output_file)
    os.remove(output_file)


async def merge_videos(event, args, client):
    """
    Merge videos.
    Usage: Reply to a video with /merge, then send other videos.
    Send /merge again to start merging.
    """
    user_id = event.sender_id
    if not user_is_allowed(user_id):
        return

    if user_id not in _merging_sessions:
        _merging_sessions[user_id] = []

    if event.is_reply:
        reply_message = await event.get_reply_message()
        if reply_message.video:
            _merging_sessions[user_id].append(reply_message)
            return await event.reply(
                f"Added video to merge queue. Send more videos or send /merge again to start merging."
            )

    if not _merging_sessions[user_id]:
        return await event.reply(
            "Please reply to at least one video to start merging."
        )

    if len(_merging_sessions[user_id]) < 2:
        return await event.reply("Please send at least two videos to merge.")

    input_files = [await event.client.download_media(m) for m in _merging_sessions[user_id]]
    output_file = f"merged_{os.path.basename(input_files[0])}"

    cmd = ["ffmpeg"]
    for f in input_files:
        cmd.extend(["-i", f])

    filter_complex = "".join(
        [f"[{i}:v] [{i}:a]" for i in range(len(input_files))]
    )
    filter_complex += f" concat=n={len(input_files)}:v=1:a=1 [v] [a]"

    cmd.extend([
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-map",
        "[a]",
        output_file,
    ])

    encoder = Encoder(f"{event.chat_id}:{event.id}", event=event)
    await encoder.start(" ".join(cmd))
    await encoder.callback(input_files[0], output_file, event, user_id)
    stdout, stderr = await encoder.await_completion()

    if stderr:
        await event.reply(f"Error during merging: ```{stderr.decode()}```")
    else:
        await event.client.send_file(event.chat_id, output_file)

    for f in input_files:
        os.remove(f)
    os.remove(output_file)
    del _merging_sessions[user_id]
