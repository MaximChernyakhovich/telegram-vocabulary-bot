from icecream import ic
import psycopg2
from pathlib import Path
import os
from dotenv import load_dotenv
# Загрузка переменных окружения из файла .env
env_path = Path(__file__).parent / ".env"  # Полный путь к .env
load_dotenv(dotenv_path=env_path)

class Database:

    def __init__(self):
        self.connection = psycopg2.connect(
                            dbname=os.environ.get("DB", "default_db"),
                            user=os.environ.get("DB_USER", "default_user"),
                            password=os.environ.get("DB_PASSWORD", "default_password"),
                            host=os.environ.get("DB_HOST", "localhost"),
                            port=os.environ.get("DB_PORT", "5432"))
        self.cursor = self.connection.cursor()
        print("Connected to the database.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self.connection:
            self.connection.close()
        print("Connected is closed.")

    def execute_query(self, query, params=None):
        if not self.connection or self.connection.closed != 0:
            self.connect()
        
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        self.connection.commit()

        # получение статуса выполнения запроса
        return self.cursor.fetchall()#self.connection.notices[0]#.split()[1]
        
    def fetch_data(self, query, params=None):
        if not self.connection or self.connection.closed != 0:
            self.connect()
        
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()