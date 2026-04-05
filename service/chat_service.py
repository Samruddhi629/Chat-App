from data_access.storage import (
    create_chat_data,
    get_all_chats_data,
    get_all_messages_data,
    get_chat_by_users,
    get_next_chat_id,
    get_user_by_id_data,
)


def create_chat(current_user: dict, data: dict):
    other_user_id = (data.get("otherUserId") or "").strip()

    if not other_user_id:
        return {"error": "otherUserId is required"}, 400

    if current_user["id"] == other_user_id:
        return {"error": "You cannot create a chat with yourself"}, 400

    other_user = get_user_by_id_data(other_user_id)
    if not other_user:
        return {"error": "Other user not found"}, 404

    existing_chat = get_chat_by_users(current_user["id"], other_user_id)
    if existing_chat:
        return {
            "message": "Chat already exists",
            "chat": existing_chat,
        }, 200

    chat = {
        "id": get_next_chat_id(),
        "users": [current_user["id"], other_user_id],
        "latestMessage": None,
    }
    create_chat_data(chat)

    return {
        "message": "Chat created successfully",
        "chat": chat,
    }, 201


def get_all_chats(current_user: dict):
    user_chats = []

    for chat in get_all_chats_data():
        if current_user["id"] not in chat["users"]:
            continue

        unseen_count = 0
        for message in get_all_messages_data():
            if (
                message["chatId"] == chat["id"]
                and message["senderId"] != current_user["id"]
                and not message["seen"]
            ):
                unseen_count += 1

        other_user_id = next(
            (user_id for user_id in chat["users"] if user_id != current_user["id"]),
            None,
        )
        other_user = get_user_by_id_data(other_user_id) if other_user_id else None

        user_chats.append(
            {
                "chat": chat,
                "otherUser": other_user,
                "unseenCount": unseen_count,
            }
        )

    return {"chats": user_chats}, 200
