# API Testing Guide (Postman)

Base URL:

```
http://127.0.0.1:5000/api/v1
```

---

## 1. Login

**POST** `/login`

Body (JSON):

```
{
  "email": "alice@example.com"
}
```

Response:

- message
- otp

---

## 2. Verify OTP

**POST** `/verify`

Body:

```
{
  "email": "alice@example.com",
  "otp": "123456"
}
```

Response:

- user
- token

---

## 3. Authorization (for protected APIs)

Header:

```
Authorization: Bearer <token>
```

---

## 4. Get Profile

**GET** `/me`

Header required

---

## 5. Get All Users

**GET** `/user/all`

---

## 6. Get Single User

**GET** `/user/<id>`

Example:

```
/user/user2
```

---

## 7. Update User

**POST** `/update/user`

Header required

Body:

```
{
  "name": "New Name"
}
```

---

## 8. Create Chat

**POST** `/chat/new`

Header required

Body:

```
{
  "otherUserId": "user2"
}
```

Response:

- chat.id (use this for messages)

---

## 9. Send Message

**POST** `/message`

Header required

Body → form-data:

```
chatId = chat1
text = Hello
```

(Optional)

```
image = file
```

---

## 10. Get Messages

**GET** `/message/<chatId>`

Header required

Example:

```
/message/chat1
```

---

## Testing Flow

1. Login
2. Verify OTP
3. Copy token
4. Add Authorization header
5. Get profile
6. Get users
7. Create chat
8. Send message
9. Get messages
