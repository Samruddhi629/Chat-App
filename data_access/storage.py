users = {
    "user1": {
        "id": "user1",
        "name": "Alice",
        "email": "alice@example.com",
        "isOnline": False,
    },
    "user2": {
        "id": "user2",
        "name": "Bob",
        "email": "bob@example.com",
        "isOnline": False,
    },
    "user3": {
        "id": "user3",
        "name": "Charlie",
        "email": "charlie@example.com",
        "isOnline": False,
    },
}

otp_store = {}
otp_rate_limit = {}
chats = {}
messages = {}

user_counter = len(users) + 1
chat_counter = 1
message_counter = 1


def get_next_user_id():
    global user_counter
    user_id = f"user{user_counter}"
    user_counter += 1
    return user_id


def get_next_chat_id():
    global chat_counter
    chat_id = f"chat{chat_counter}"
    chat_counter += 1
    return chat_id


def get_next_message_id():
    global message_counter
    message_id = f"message{message_counter}"
    message_counter += 1
    return message_id


def get_all_users_data():
    return list(users.values())


def get_user_by_id_data(user_id):
    return users.get(user_id)


def get_user_by_email(email):
    for user in users.values():
        if user["email"] == email:
            return user
    return None


def save_user(user):
    users[user["id"]] = user
    return user


def update_user_name(user_id, name):
    users[user_id]["name"] = name
    return users[user_id]


def get_otp_record(email):
    return otp_store.get(email)


def save_otp_record(email, record):
    otp_store[email] = record


def delete_otp_record(email):
    otp_store.pop(email, None)


def get_rate_limit_record(email):
    return otp_rate_limit.get(email)


def save_rate_limit_record(email, record):
    otp_rate_limit[email] = record


def create_chat_data(chat):
    chats[chat["id"]] = chat
    return chat


def get_chat_by_id_data(chat_id):
    return chats.get(chat_id)


def get_all_chats_data():
    return list(chats.values())


def get_chat_by_users(user_one_id, user_two_id):
    target_users = sorted([user_one_id, user_two_id])

    for chat in chats.values():
        if sorted(chat["users"]) == target_users:
            return chat
    return None


def update_chat_latest_message(chat_id, latest_message):
    if chat_id in chats:
        chats[chat_id]["latestMessage"] = latest_message


def save_message(message):
    messages[message["id"]] = message
    return message


def get_all_messages_data():
    return list(messages.values())


def update_messages_seen(message_ids):
    for message_id in message_ids:
        if message_id in messages:
            messages[message_id]["seen"] = True
