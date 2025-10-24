#    This file is part of the Encoder distribution.
#    Copyright (c) 2023 Danish_00, Nubuki-all
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in
# <https://github.com/Nubuki-all/Enc/blob/main/License> .

import asyncio
import itertools

from pyrogram import filters

from . import LOGS, conf, events, pyro, re, tele
from .startup.after import on_startup
from .utils.msg_utils import event_handler
from .workers.handlers.admin import (
    clear_queue,
    restart_bot,
    view_queue,
)
from .workers.handlers.admin_config import (
    set_audio_bitrate,
    set_crf,
    set_preset,
    set_video_codec,
)
from .workers.handlers.admin_adv import (
    add_channel,
    delete_channel,
    fsub_mode,
    list_channels,
    add_paid_user,
    remove_paid_user,
    list_paid_users,
    update_bot,
)
from .workers.handlers.shortner import (
    set_shortner,
    set_shortlink1,
    set_shortlink2,
    set_tutorial1,
)
from .workers.handlers.audio import (
    add_audio,
    extract_audio,
    remove_audio,
)
from .workers.handlers.dev import bash
from .workers.handlers.dev import eval as eval_
from .workers.handlers.dev import eval_message_p
from .workers.handlers.e_callbacks import pres, skip, skip_jobs, stats
from .workers.handlers.encode import (
    encode_1080p,
    encode_144p,
    encode_2160p,
    encode_240p,
    encode_360p,
    encode_480p,
    encode_720p,
    encode_all,
)
from .workers.handlers.manage import (
    allowgroupenc,
    auto_rename,
    change,
    check,
    clean,
    custom_rename,
    del_auto_rename,
    discap,
    fc_forward,
)
from .workers.handlers.manage import filter as filter_
from .workers.handlers.manage import (
    get_mux_args,
    nuke,
    pause,
    reffmpeg,
    rmfilter,
    rss_handler,
    save_thumb,
    set_mux_args,
    update2,
    v_auto_rename,
    version2,
    vfilter,
)
from .workers.handlers.misc import (
    get_media_info,
    set_media_type,
    upload_file,
)
from .workers.handlers.queue import (
    addqueue,
    edit_batch,
    enleech,
    enleech2,
    enselect,
    pencode,
    pencode_callback,
)
from .workers.handlers.rebut import (
    en_airing,
    en_anime,
    en_list,
    en_mux,
    en_rename,
    getlogs,
)
from .workers.handlers.stuff import help as help_
from .workers.handlers.stuff import start, status, temp_auth, temp_unauth, up
from .workers.handlers.subtitles import (
    add_hardcoded_subtitles,
    add_subtitles,
    extract_subtitles,
    remove_subtitles,
)
from .workers.handlers.thumbnail import (
    delete_thumbnail,
    extract_thumbnail,
    get_thumbnail,
    set_thumbnail,
)
from .workers.handlers.video_manipulation import (
    compress_video,
    crop_video,
    cut_video,
    merge_videos,
    rename_video,
)
from .workers.handlers.watermark import (
    add_watermark,
    get_watermark,
    set_watermark,
    spoiler,
)

from .config_manager import load_config

cmd_suffix = conf.CMD_SUFFIX.strip()
LOGS.info("Starting...")

load_config()


######## Connect ########


try:
    tele.start(bot_token=conf.BOT_TOKEN)
    pyro.start()
except Exception as er:
    LOGS.info(er)


####### CMD FILTER ########
async def get_me():
    globals()["me"] = await tele.get_me()


loop = asyncio.get_event_loop()
loop.run_until_complete(get_me())

LOGS.info(f"@{me.username} is ready!")


def command(commands: list, prefixes: list = ["/"]):
    while len(commands) < len(prefixes):
        commands.append(commands[-1])
    pattern = ""
    for command, prefix in itertools.zip_longest(commands, prefixes, fillvalue="/"):
        if cmd_suffix:
            command += cmd_suffix
        pattern += rf"{prefix}{command}(?:@{me.username})?(?!\S)|"
    return pattern.rstrip("|")


####### GENERAL CMDS ########


@tele.on(events.NewMessage(pattern=command(["start"])))
async def _(e):
    await event_handler(e, start)


@tele.on(events.NewMessage(pattern="/ping"))
async def _(e):
    await event_handler(e, up)


@tele.on(events.NewMessage(pattern=command(["help"])))
async def _(e):
    await event_handler(e, help_)


@tele.on(events.NewMessage(pattern=command(["status"])))
async def _(e):
    await event_handler(e, status)


####### THUMBNAIL CMDS #######


@tele.on(events.NewMessage(pattern=command(["setthumb"])))
async def _(e):
    await event_handler(e, set_thumbnail)


@tele.on(events.NewMessage(pattern=command(["getthumb"])))
async def _(e):
    await event_handler(e, get_thumbnail)


@tele.on(events.NewMessage(pattern=command(["delthumb"])))
async def _(e):
    await event_handler(e, delete_thumbnail)


@tele.on(events.NewMessage(pattern=command(["extract_thumb"])))
async def _(e):
    await event_handler(e, extract_thumbnail)


####### WATERMARK CMDS #######


@tele.on(events.NewMessage(pattern=command(["setwatermark"])))
async def _(e):
    await event_handler(e, set_watermark)


@tele.on(events.NewMessage(pattern=command(["getwatermark"])))
async def _(e):
    await event_handler(e, get_watermark)


@tele.on(events.NewMessage(pattern=command(["addwatermark"])))
async def _(e):
    await event_handler(e, add_watermark)


@tele.on(events.NewMessage(pattern=command(["spoiler"])))
async def _(e):
    await event_handler(e, spoiler)


####### VIDEO MANIPULATION CMDS #######


@tele.on(events.NewMessage(pattern=command(["compress"])))
async def _(e):
    await event_handler(e, compress_video)


@tele.on(events.NewMessage(pattern=command(["cut"])))
async def _(e):
    await event_handler(e, cut_video)


@tele.on(events.NewMessage(pattern=command(["crop"])))
async def _(e):
    await event_handler(e, crop_video)


@tele.on(events.NewMessage(pattern=command(["merge"])))
async def _(e):
    await event_handler(e, merge_videos)


####### ENCODING & RESOLUTION CMDS #######


@tele.on(events.NewMessage(pattern=command(["144p"])))
async def _(e):
    await event_handler(e, encode_144p)


@tele.on(events.NewMessage(pattern=command(["240p"])))
async def _(e):
    await event_handler(e, encode_240p)


@tele.on(events.NewMessage(pattern=command(["360p"])))
async def _(e):
    await event_handler(e, encode_360p)


@tele.on(events.NewMessage(pattern=command(["480p"])))
async def _(e):
    await event_handler(e, encode_480p)


@tele.on(events.NewMessage(pattern=command(["720p"])))
async def _(e):
    await event_handler(e, encode_720p)


@tele.on(events.NewMessage(pattern=command(["1080p"])))
async def _(e):
    await event_handler(e, encode_1080p)


@tele.on(events.NewMessage(pattern=command(["2160p"])))
async def _(e):
    await event_handler(e, encode_2160p)


@tele.on(events.NewMessage(pattern=command(["all"])))
async def _(e):
    await event_handler(e, encode_all)


####### SUBTITLE CMDS #######


@tele.on(events.NewMessage(pattern=command(["sub"])))
async def _(e):
    await event_handler(e, add_subtitles)


@tele.on(events.NewMessage(pattern=command(["hsub"])))
async def _(e):
    await event_handler(e, add_hardcoded_subtitles)


@tele.on(events.NewMessage(pattern=command(["rsub"])))
async def _(e):
    await event_handler(e, remove_subtitles)


@tele.on(events.NewMessage(pattern=command(["extract_sub"])))
async def _(e):
    await event_handler(e, extract_subtitles)


####### AUDIO CMDS #######


@tele.on(events.NewMessage(pattern=command(["extract_audio"])))
async def _(e):
    await event_handler(e, extract_audio)


@tele.on(events.NewMessage(pattern=command(["addaudio"])))
async def _(e):
    await event_handler(e, add_audio)


@tele.on(events.NewMessage(pattern=command(["remaudio"])))
async def _(e):
    await event_handler(e, remove_audio)


####### MISC CMDS #######


@tele.on(events.NewMessage(pattern=command(["setmedia"])))
async def _(e):
    await event_handler(e, set_media_type)




@tele.on(events.NewMessage(pattern=command(["mediainfo"])))
async def _(e):
    await event_handler(e, get_media_info)


@tele.on(events.NewMessage(pattern=command(["upload"])))
async def _(e):
    await event_handler(e, upload_file)


####### ADMIN CMDS #######


@tele.on(events.NewMessage(pattern=command(["restart"])))
async def _(e):
    await event_handler(e, restart_bot)


@tele.on(events.NewMessage(pattern=command(["queue"])))
async def _(e):
    await event_handler(e, view_queue)


@tele.on(events.NewMessage(pattern=command(["clear"])))
async def _(e):
    await event_handler(e, clear_queue)


@tele.on(events.NewMessage(pattern=command(["audio"])))
async def _(e):
    await event_handler(e, set_audio_bitrate)


@tele.on(events.NewMessage(pattern=command(["codec"])))
async def _(e):
    await event_handler(e, set_video_codec)


@tele.on(events.NewMessage(pattern=command(["preset"])))
async def _(e):
    await event_handler(e, set_preset)


@tele.on(events.NewMessage(pattern=command(["crf"])))
async def _(e):
    await event_handler(e, set_crf)


@tele.on(events.NewMessage(pattern=command(["addchnl"])))
async def _(e):
    await event_handler(e, add_channel)


@tele.on(events.NewMessage(pattern=command(["delchnl"])))
async def _(e):
    await event_handler(e, delete_channel)


@tele.on(events.NewMessage(pattern=command(["listchnl"])))
async def _(e):
    await event_handler(e, list_channels)


@tele.on(events.NewMessage(pattern=command(["addpaid"])))
async def _(e):
    await event_handler(e, add_paid_user)


@tele.on(events.NewMessage(pattern=command(["rempaid"])))
async def _(e):
    await event_handler(e, remove_paid_user)


@tele.on(events.NewMessage(pattern=command(["listpaid"])))
async def _(e):
    await event_handler(e, list_paid_users)


@tele.on(events.NewMessage(pattern=command(["fsub_mode"])))
async def _(e):
    await event_handler(e, fsub_mode)


@tele.on(events.NewMessage(pattern=command(["update"])))
async def _(e):
    await event_handler(e, update_bot)


@tele.on(events.NewMessage(pattern=command(["shortner"])))
async def _(e):
    await event_handler(e, set_shortner)


@tele.on(events.NewMessage(pattern=command(["shortlink1"])))
async def _(e):
    await event_handler(e, set_shortlink1)


@tele.on(events.NewMessage(pattern=command(["shortlink2"])))
async def _(e):
    await event_handler(e, set_shortlink2)


@tele.on(events.NewMessage(pattern=command(["tutorial1"])))
async def _(e):
    await event_handler(e, set_tutorial1)


@tele.on(events.NewMessage(pattern=command(["rename"])))
async def _(e):
    await event_handler(e, rename_video)


####### POWER CMDS #######


@tele.on(events.NewMessage(pattern=command(["nuke"])))
async def _(e):
    await event_handler(e, nuke)


@pyro.on_message(filters.incoming & filters.command([f"update{cmd_suffix}"]))
async def _(pyro, message):
    await update2(pyro, message)


@tele.on(events.NewMessage(pattern=command(["clean", "cancelall"])))
async def _(e):
    await event_handler(e, clean)


@tele.on(events.NewMessage(pattern=command(["clear"])))
async def _(e):
    await event_handler(e, clearqueue, require_args=True)


@tele.on(events.NewMessage(pattern=command(["permit"])))
async def _(e):
    await event_handler(e, temp_auth, pyro)


@tele.on(events.NewMessage(pattern=command(["unpermit"])))
async def _(e):
    await event_handler(e, temp_unauth, pyro)


@tele.on(events.NewMessage(pattern=command(["groupenc"])))
async def _(e):
    await event_handler(e, allowgroupenc)


@tele.on(events.NewMessage(pattern=command(["parse"])))
async def _(e):
    await event_handler(e, discap, require_args=True)


@tele.on(events.NewMessage(pattern=command(["v"])))
async def _(e):
    await event_handler(e, version2)


@tele.on(events.NewMessage(pattern=command(["filter"])))
async def _(e):
    await event_handler(e, filter_, require_args=True)


@tele.on(events.NewMessage(pattern=command(["vfilter"])))
async def _(e):
    await event_handler(e, vfilter)


@tele.on(events.NewMessage(pattern=command(["delfilter"])))
async def _(e):
    await event_handler(e, rmfilter)


@tele.on(events.NewMessage(pattern=command(["mset"])))
async def _(e):
    await event_handler(e, set_mux_args, require_args=True)


@tele.on(events.NewMessage(pattern=command(["mget"])))
async def _(e):
    await event_handler(e, get_mux_args)


@tele.on(events.NewMessage(pattern=command(["get"])))
async def _(e):
    await event_handler(e, check)


@tele.on(events.NewMessage(pattern=command(["set"])))
async def _(e):
    await event_handler(e, change, require_args=True)


@tele.on(events.NewMessage(pattern=command(["reset"])))
async def _(e):
    await event_handler(e, reffmpeg)


@tele.on(events.NewMessage(pattern=command(["lock", "pause"])))
async def _(e):
    await event_handler(e, pause)


@tele.on(events.NewMessage(pattern=command(["rss"])))
async def _(e):
    await event_handler(e, rss_handler, require_args=True)


######## Callbacks #########


@tele.on(events.callbackquery.CallbackQuery(data=re.compile(b"stats(.*)")))
async def _(e):
    await stats(e)


@tele.on(events.callbackquery.CallbackQuery(data=re.compile(b"pres(.*)")))
async def _(e):
    await pres(e)


@tele.on(events.callbackquery.CallbackQuery(data=re.compile(b"skip(.*)")))
async def _(e):
    await skip(e)


@tele.on(events.callbackquery.CallbackQuery(data=re.compile(b"jskip(.*)")))
async def _(e):
    await skip_jobs(e)


@tele.on(events.callbackquery.CallbackQuery(data=re.compile(b"dl_stat(.*)")))
async def _(e):
    await dl_stat(e)


@tele.on(events.callbackquery.CallbackQuery(data=re.compile(b"cancel_dl(.*)")))
async def _(e):
    await cancel_dl(e)




@tele.on(events.callbackquery.CallbackQuery(data=re.compile(b"quality_(.*)")))
async def _(e):
    await pencode_callback(e)


########## Direct ###########


@tele.on(events.NewMessage(pattern=command(["eval"])))
async def _(e):
    await event_handler(e, eval_, pyro, True)


@tele.on(events.NewMessage(pattern=command(["leech", "l"])))
async def _(e):
    await event_handler(e, enleech, pyro)


@tele.on(events.NewMessage(pattern=command(["qbleech", "ql"])))
async def _(e):
    await event_handler(e, enleech2, pyro)


@tele.on(events.NewMessage(pattern=command(["list"], ["/", "!"])))
async def _(e):
    await event_handler(e, en_list, pyro, require_args=True)


@tele.on(events.NewMessage(pattern=command(["select", "s"])))
async def _(e):
    await event_handler(e, enselect, pyro, require_args=True)


@tele.on(events.NewMessage(pattern=command(["add", "releech"])))
async def _(e):
    await event_handler(e, addqueue, pyro)


@tele.on(events.NewMessage(pattern=command(["m", "mediainfo"])))
async def _(e):
    await event_handler(e, getminfo, pyro)


@tele.on(events.NewMessage(pattern=command(["download", "dl"], ["/", "!", "/"])))
async def _(e):
    await event_handler(e, en_download, pyro)


@tele.on(events.NewMessage(pattern=command(["upload", "ul"], ["/", "!", "/"])))
async def _(e):
    await event_handler(e, en_upload, pyro, require_args=True)


@tele.on(events.NewMessage(pattern=command(["rename", "rn"], ["/", "!", "/"])))
async def _(e):
    await event_handler(e, en_rename, pyro)


@tele.on(events.NewMessage(pattern=command(["mux"], ["/", "!"])))
async def _(e):
    await event_handler(e, en_mux, pyro, require_args=True)


@pyro.on_message(filters.incoming & filters.command([f"peval{cmd_suffix}"]))
async def _(pyro, message):
    await event_handler(message, eval_message_p, tele, require_args=True)


@pyro.on_message(
    filters.incoming
    & filters.command([f"fforward{cmd_suffix}", f"forward{cmd_suffix}"])
)
async def _(pyro, message):
    await event_handler(message, fc_forward)


@tele.on(events.NewMessage(pattern=command(["bash"])))
async def _(e):
    await event_handler(e, bash, require_args=True)


@tele.on(events.NewMessage(pattern=command(["airing"])))
async def _(e):
    await event_handler(e, en_airing, require_args=True)


@tele.on(events.NewMessage(pattern=command(["anime"])))
async def _(e):
    await event_handler(e, en_anime, require_args=True)


@tele.on(events.NewMessage(pattern=command(["setrename"])))
async def _(e):
    await event_handler(e, custom_rename, require_args=True)


@tele.on(events.NewMessage(pattern=command(["name"])))
async def _(e):
    await event_handler(e, auto_rename, require_args=True)


@tele.on(events.NewMessage(pattern=command(["vname"])))
async def _(e):
    await event_handler(e, v_auto_rename)


@tele.on(events.NewMessage(pattern=command(["delname"])))
async def _(e):
    await event_handler(e, del_auto_rename, require_args=True)


@tele.on(events.NewMessage(pattern=command(["queue"], ["/", "!"])))
async def _(e):
    await event_handler(e, listqueue)


@tele.on(events.NewMessage(pattern=command(["batch", "gb"])))
async def _(e):
    await event_handler(e, edit_batch, pyro)


######## DEBUG #########


@tele.on(events.NewMessage(pattern=command(["logs"])))
async def _(e):
    await event_handler(e, getlogs)


########## AUTO ###########


# @tele.on(events.NewMessage(incoming=True))
# async def _(e):
#    await encod(e)


@pyro.on_message(filters.incoming & (filters.video | filters.document))
async def _(pyro, message):
    await pencode(message)


########### Start ############

LOGS.info(f"{me.first_name} has started.")
with tele:
    tele.loop.run_until_complete(on_startup())
    tele.loop.run_forever()
