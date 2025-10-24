import pickle

from bot import _bot, local_cdb, local_qdb, local_qdb2, local_rdb, local_udb

from .bot_utils import list_to_str
from .os_utils import file_exists


class LightMessage:
    def __init__(self, message_id, chat_id):
        self.id = message_id
        self.chat = self
        self.chat_id = chat_id

def load_local_db():
    if file_exists(local_qdb):
        with open(local_qdb, "rb") as file:
            local_queue = pickle.load(file)

        for key, value in local_queue.items():
            name, (sender_id, message_info), rest = value[0], value[1], value[2:]
            if isinstance(message_info, tuple):
                message_id, chat_id = message_info
                # Recreate a light version of the message object
                message = LightMessage(message_id, chat_id)
                restored_value = [name, (sender_id, message)] + list(rest)
                _bot.queue[key] = restored_value
            else:
                _bot.queue[key] = value

    if file_exists(local_qdb2):
        with open(local_qdb2, "rb") as file:
            local_queue = pickle.load(file)
        _bot.batch_queue.update(local_queue)

    if file_exists(local_rdb):
        with open(local_rdb, "rb") as file:
            local_dict = pickle.load(file)
        _bot.rss_dict.update(local_dict)

    if file_exists(local_udb):
        with open(local_udb, "rb") as file:
            local_users = pickle.load(file)
        for user in local_users.split():
            if user not in _bot.temp_users:
                _bot.temp_users.append(user)

    if file_exists(local_cdb):
        with open(local_cdb, "rb") as file:
            local_format = pickle.load(file)
        _bot.custom_rename = local_format


def save2db_lcl():
    # Sanitize the queue to make it pickleable
    sanitized_queue = {}
    for key, value in _bot.queue.items():
        # value is a list: [name, (sender_id, message), (v, f, m, n, au, quality)]
        # The 'message' object is not pickleable, so we replace it with its ID and chat ID
        name, (sender_id, message), rest = value[0], value[1], value[2:]
        if message:
            sanitized_message = (message.id, message.chat.id)
            sanitized_value = [name, (sender_id, sanitized_message)] + list(rest)
            sanitized_queue[key] = sanitized_value
        else:
            sanitized_queue[key] = value

    with open(local_qdb, "wb") as file:
        pickle.dump(sanitized_queue, file)
    with open(local_qdb2, "wb") as file:
        pickle.dump(_bot.batch_queue, file)


def save2db_lcl2(db):
    if db is None:
        with open(local_udb, "wb") as file:
            pickle.dump(list_to_str(_bot.temp_users), file)
    elif db == "rss":
        with open(local_rdb, "wb") as file:
            pickle.dump(_bot.rss_dict, file)
    elif db == "cus_rename":
        with open(local_cdb, "wb") as file:
            pickle.dump(_bot.custom_rename, file)
