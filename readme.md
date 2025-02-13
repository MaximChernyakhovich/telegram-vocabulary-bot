# Telegram Vocabulary Bot

Telegram Vocabulary Bot — это телеграм-бот для изучения английских слов. Позволяет пользователям добавлять слова, проходить тесты и запоминать новые слова с помощью повторений.

## Функциональность
- Добавление слов в личный словарь
- Просмотр списка изучаемых слов
- Прохождение тестов для запоминания
- Автоматические напоминания о повторении слов

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/MaximChernyakhovich/telegram-vocabulary-bot.git
cd telegram-vocabulary-bot
```

### 2. Создание виртуального окружения (опционально)
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate  # Для Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

## Конфигурация
Создайте файл `.env` в корневой директории и укажите параметры:
```
DB=vocabulary_db
DB_USER=admin
DB_PASSWORD=securepassword
DB_HOST=localhost
DB_PORT=5432
API_KEY=your_api_key_here
```

## Запуск
```bash
python bot.py
```

## Зависимости (requirements.txt)
```
pyTelegramBotAPI==4.23.0
psycopg2
icecream
python-dotenv
requests
pathlib
```