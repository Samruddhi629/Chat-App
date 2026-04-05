from data_access.storage import (
    get_all_messages_data,
    get_chat_by_id_data,
    get_next_message_id,
    get_user_by_id_data,
    save_message,
    update_chat_latest_message,
    update_messages_seen,
)


def send_message(current_user: dict, data: dict):
    chat_id = (data.get("chatId") or "").strip()
    text = (data.get("text") or "").strip()
    image = data.get("image")

    if not chat_id:
        return {"error": "chatId is required"}, 400

    if not text and not image:
        return {"error": "Either text or image is required"}, 400

    chat = get_chat_by_id_data(chat_id)
    if not chat:
        return {"error": "Chat not found"}, 404

    if current_user["id"] not in chat["users"]:
        return {"error": "You are not part of this chat"}, 403

    image_data = None
    message_type = "text"

    if image:
        message_type = "image"
        image_data = {
            "filename": image.filename,
            "contentType": image.content_type,
        }

    message = {
        "id": get_next_message_id(),
        "chatId": chat_id,
        "senderId": current_user["id"],
        "text": text,
        "image": image_data,
        "messageType": message_type,
        "seen": False,
    }
    save_message(message)

    preview_text = text if text else "Image"
    update_chat_latest_message(
        chat_id,
        {
            "text": preview_text,
            "senderId": current_user["id"],
        },
    )

    return {
        "message": "Message sent successfully",
        "data": message,
    }, 201


def get_messages(current_user: dict, chat_id: str):
    chat = get_chat_by_id_data(chat_id)

    if not chat:
        return {"error": "Chat not found"}, 404

    if current_user["id"] not in chat["users"]:
        return {"error": "You are not part of this chat"}, 403

    chat_messages = []
    unseen_message_ids = []

    for message in get_all_messages_data():
        if message["chatId"] != chat_id:
            continue

        if message["senderId"] != current_user["id"] and not message["seen"]:
            unseen_message_ids.append(message["id"])

        chat_messages.append(message)

    if unseen_message_ids:
        update_messages_seen(unseen_message_ids)
        for message in chat_messages:
            if message["id"] in unseen_message_ids:
                message["seen"] = True

    other_user_id = next(
        (user_id for user_id in chat["users"] if user_id != current_user["id"]),
        None,
    )
    other_user = get_user_by_id_data(other_user_id) if other_user_id else None

    return {
        "messages": chat_messages,
        "otherUser": other_user,
    }, 200
