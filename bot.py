import telebot
import requests
from telebot import types
from user import User
from vocabulary import Vocabulary
from keyboards import Keyboards
from vocabulary_handler import VocabularyHandler
import os
from dotenv import load_dotenv
from icecream import ic
import time
from pathlib import Path

# Загрузка переменных окружения из файла .env
env_path = Path(__file__).parent / ".env"  # Полный путь к .env
load_dotenv(dotenv_path=env_path)

# сделать список актуальных слов для изучения и выученных слов

def google_trans(word):
    # Можно использовать для бота в качестве быстрого переводчика
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "en",  # Исходный язык
        "tl": "ru",  # Язык перевода
        "dt": "t",
        "q": word # Текст для перевода
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        translated_text = response.json()[0][0][0]
    else:
        print("Error:", response.status_code, response.text)
    return translated_text

class BotHandler:
    def __init__(self, api_token_key):
        # Инициализация бота с использованием API токена
        self.bot = telebot.TeleBot(api_token_key)
        self.user_instance = None
        self.operations_instance = None
        self.vocabulary_handler = VocabularyHandler(self.bot)
        self.register_handlers()

    def handle_start(self, message):
        # Обработка команды /start
        chat_id = message.chat.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        self.bot.send_message(chat_id, f'Добрый день, {first_name}!')
        self.user_instance = User(tg_id=chat_id, firstname=first_name, lastname=last_name, tg_nick=username)
        user_data = self.user_instance.fetch_user()
        ic(user_data)

    def request_words_to_add(self, message):
        # Запрос списка слов для добавления
        self.bot.send_message(message.chat.id, 'Введите список слов:')
        user_data = {}
        self.bot.register_next_step_handler(message, lambda msg: self.process_words_addition(msg, user_data))
        ic(user_data)

    def process_words_addition(self, message, user_data):
        # Обработка добавленных слов
        user_data['words'] = ''.join(message.text.split()).split(',')
        vc = Vocabulary(tg_id=message.chat.id, words=user_data['words'])
        vc.add_words()
        self.bot.send_message(message.chat.id, "Слова добавлены!")
        ic(user_data)

    def request_words_to_remove(self, message):
        # Запрос списка слов для удаления
        self.bot.send_message(message.chat.id, 'Введите список слов для удаления:')
        user_data = {}
        self.bot.register_next_step_handler(message, lambda msg: self.process_words_removal(msg, user_data))
        ic(user_data)

    def process_words_removal(self, message, user_data):
        # Обработка удаления слов
        user_data['words'] = ''.join(message.text.split()).split(',')
        vc = Vocabulary(tg_id=message.chat.id, words=user_data['words'])
        vc.delete_words()
        self.bot.send_message(message.chat.id, "Слова удалены!")
        ic(user_data)

    def request_translation(self, message):
        # Запрос слова или фразы для перевода
        self.bot.send_message(message.chat.id, 'Введите слово или фразу:')
        user_data = {}
        self.bot.register_next_step_handler(message, lambda msg: self.process_translation(msg, user_data))
        ic(user_data)

    def process_translation(self, message, user_data):
        # Обработка перевода
        user_data['translation'] = message.text
        self.bot.send_message(message.chat.id, f"Перевод:\n\n{google_trans(user_data['translation'])}")
        ic(user_data)

    def send_vocabulary_list(self, message):
        # Отправка списка слов пользователя
        self.vocabulary_handler.send_word_list(message)

    def handle_test_answer(self, call):
        answer = call.data.split("_", 1)[1]  # Получаем ответ пользователя
        word = "apple"  # Слово для перевода
        correct_answer = 'яблоко'  # Правильный ответ
        if answer == correct_answer:
            # Обновляем сообщение, чтобы показать правильный ответ
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"Как переводится слово *{word}*?\n\n✅ Правильно! Ответ: {correct_answer}",
                parse_mode="Markdown"
            )
        else:
            # Обновляем сообщение, чтобы показать неправильный ответ
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"Как переводится слово *{word}*?\n\n❌ Неправильно!",
                parse_mode="Markdown"
            )

    def register_handlers(self):
        # Обрабатываем все ответы на тесты
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("test_"))(self.handle_test_answer)

    def start_polling(self):
        # Запуск процесса polling
        while True:
            #try:
                self.bot.polling(none_stop=True, interval=1)
            # except:
            #     print('restart')
            #     time.sleep(2)


api_token_key = os.getenv("API_KEY")
bot_handler = BotHandler(api_token_key)

commands = {
    'start': bot_handler.handle_start,
    'add_words': bot_handler.request_words_to_add,
    'remove_words': bot_handler.request_words_to_remove,
    'translate': bot_handler.request_translation,
    'vocabulary': bot_handler.send_vocabulary_list
}

for cmd, func in commands.items():
    bot_handler.bot.message_handler(commands=[cmd])(func)

bot_handler.start_polling()