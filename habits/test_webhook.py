import requests
import json

url = "http://localhost:8000/telegram-webhook/"

# Данные для имитации Telegram сообщения
data = {
    "message": {
        "text": "/start",
        "chat": {
            "id": 123456789  # любой chat_id
        }
    }
}

# Отправляем POST запрос
response = requests.post(
    url,
    headers={"Content-Type": "application/json"},
    data=json.dumps(data)
)

print("Status Code:", response.status_code)
print("Response:", response.text)