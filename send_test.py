import requests
import random
from pathlib import Path
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env
env_path = Path(__file__).parent / ".env"  # Полный путь к .env
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("API_KEY")  # Чтение токена из .env
CHAT_ID = 123 # ID чата для отправки теста

word = "apple"
correct_answer = "яблоко"
options = ["груша", "банан", "яблоко", "виноград"]
random.shuffle(options)

# Создание инлайн-кнопок
keyboard = {"inline_keyboard": [options[i:i+2] for i in range(0, len(options), 2)]}
keyboard["inline_keyboard"] = [
    [{"text": option, "callback_data": f"test_{option}"} for option in row] for row in keyboard["inline_keyboard"]
]

# Формируем запрос к боту
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": f"Как переводится слово *{word}*?",
    "parse_mode": "Markdown",
    "reply_markup": keyboard
}

response = requests.post(url, json=payload)
print(response.json())  # Проверяем результат отправки