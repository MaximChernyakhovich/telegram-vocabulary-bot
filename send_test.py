import requests
import random
from pathlib import Path
from dotenv import load_dotenv
import os

class TranslationTestSender:
    """Бот для отправки тестов по переводу в Telegram."""

    def __init__(self, token: str, chat_id: int):
        """Инициализация бота с токеном и ID чата."""
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    def _generate_keyboard(self, options: list) -> dict:
        """Создает инлайн-клавиатуру из списка вариантов."""
        random.shuffle(options)
        keyboard = {
            "inline_keyboard": [
                [{"text": option, "callback_data": f"test_{option}"} for option in options[i:i + 2]]
                for i in range(0, len(options), 2)
            ]
        }
        return keyboard

    def send_translation_test(self, word: str, correct_answer: str, options: list):
        """
        Отправляет тест по переводу в Telegram с инлайн-кнопками.

        :param word: Слово для перевода.
        :param correct_answer: Правильный ответ.
        :param options: Список вариантов ответа.
        """
        if correct_answer not in options:
            options.append(correct_answer)
        
        keyboard = self._generate_keyboard(options)
        
        payload = {
            "chat_id": self.chat_id,
            "text": f"Как переводится слово *{word}*?",
            "parse_mode": "Markdown",
            "reply_markup": keyboard
        }

        response = requests.post(f"{self.base_url}/sendMessage", json=payload)
        
        # Логируем результат отправки
        if response.ok:
            print("Сообщение успешно отправлено")
        else:
            print(f"Ошибка отправки: {response.status_code} - {response.text}")


if __name__ == "__main__":
    # Загрузка переменных окружения
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path)

    token = os.getenv("API_KEY")
    chat_id = 123

    # Инициализация бота
    bot = TranslationTestSender(token=token, chat_id=chat_id)

    # Пример теста
    word = "apple"
    correct_answer = "яблоко"
    options = ["груша", "банан", "виноград"]

    # Отправка теста
    bot.send_translation_test(word, correct_answer, options)