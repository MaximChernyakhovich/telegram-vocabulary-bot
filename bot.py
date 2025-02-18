import telebot
import requests
from telebot import types
from user import User
from vocabulary import Vocabulary
from keyboards import Keyboards
from translator import Translator
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
        self.bot.register_next_step_handler(message, lambda msg: self.process_translation(msg))
        ic(user_data)

    def process_translation(self, message):
        # Обработка перевода слова или фразы
        text = message.text
        translator = Translator()
        translation = Translator().translate(text) 
        detect_lang = translator.detect_language(text)

        # Добавляем инлайновую клавиатуру
        keyboard = types.InlineKeyboardMarkup()
        add_button = types.InlineKeyboardButton(
            text="Добавить в словарь",  callback_data=f"translate_add_word:{text}:{translation}"
        )
        keyboard.add(add_button)
        
        if len(text.split()) == 1:
            if detect_lang == 'en':
                self.bot.send_message(message.chat.id, f"Перевод слова '{text}':\n\n{translation}", reply_markup=keyboard)
            else:
                self.bot.send_message(message.chat.id, f"Перевод слова '{text}':\n\n{translation}")
        else:
            self.bot.send_message(message.chat.id, f"Перевод текста:\n\n{translation}")

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
        # Регистрация всех callback handlers
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("test_"))(self.handle_test_answer)
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("translate_add_word:"))(self.handle_translate_add_word)

    def handle_translate_add_word(self, call):
        try:
            # Извлечение слова и перевода из callback_data
            _, word, translation = call.data.split(':')

            # Логика добавления слова в словарь
            vc = Vocabulary(tg_id=call.message.chat.id, words=[word])
            vc.add_words()

            # Обновляем сообщение с подтверждением добавления
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"Слово '{word}' добавлено в ваш словарь!"
            )
        except Exception as e:
            # Логирование ошибок
            self.bot.send_message(call.message.chat.id, "Произошла ошибка при добавлении слова.")
            print(f"Ошибка при обработке перевода: {e}")

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