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

from bot.utils.db_utils import save2db2

quality_settings = {}


def set_quality(user_id, new_quality):
    from bot.startup.before import qualitydb

    if qualitydb:
        qualitydb[user_id] = new_quality
        save2db2(qualitydb, "quality")
    else:
        quality_settings[user_id] = new_quality


def get_quality(user_id):
    from bot.startup.before import qualitydb

    if qualitydb:
        return qualitydb.get(user_id)
    else:
        return quality_settings.get(user_id)
