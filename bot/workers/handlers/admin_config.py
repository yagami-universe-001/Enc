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


async def set_audio_bitrate(event, args, client):
    """
    Set the audio bitrate.
    Usage: /audio <bitrate>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply(f"Current audio bitrate: `{conf.AUDIO_BITRATE}`")
    conf.AUDIO_BITRATE = args
    save_config()
    await event.reply(f"Audio bitrate set to `{args}`.")


async def set_video_codec(event, args, client):
    """
    Set the video codec.
    Usage: /codec <codec>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply(f"Current video codec: `{conf.VIDEO_CODEC}`")
    conf.VIDEO_CODEC = args
    save_config()
    await event.reply(f"Video codec set to `{args}`.")


async def set_preset(event, args, client):
    """
    Set the preset.
    Usage: /preset <preset>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply(f"Current preset: `{conf.PRESET}`")
    conf.PRESET = args
    save_config()
    await event.reply(f"Preset set to `{args}`.")


async def set_crf(event, args, client):
    """
    Set the CRF.
    Usage: /crf <crf>
    """
    if not user_is_owner(event.sender_id):
        return await event.reply("You are not authorized to use this command.")
    if not args:
        return await event.reply(f"Current CRF: `{conf.CRF}`")
    conf.CRF = args
    save_config()
    await event.reply(f"CRF set to `{args}`.")
