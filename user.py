from icecream import ic
from database import Database

class User:
    def __init__(self, tg_id: int, firstname: str, lastname: str, tg_nick: str):
        self.tg_id = tg_id
        self.firstname = firstname
        self.lastname = lastname
        self.tg_nick = tg_nick

    # Подключение к БД
    def db_connect(self):
        return Database()

    def __str__(self):
        return f"User ID: {self.tg_id}\nName: {self.firstname} {self.lastname}\nUsername: {self.tg_nick}"

    def create_profile(self):
        db = self.db_connect()

        with db as conn:
            # вызов процедуры add_user
            query = 'CALL add_user (%s, %s, %s, %s);'

            user_params = (self.tg_id, self.firstname, self.lastname, self.tg_nick)
            conn.execute_query(query, user_params)
            ic(user_params)

    def fetch_user(self):
        db = self.db_connect()

        with db as conn:
            # нужно заменить SQL-запросы на процедуры
            # проверка наличия пользователя в БД
            check_id = conn.fetch_data('''
                                        SELECT 
                                            CASE 
                                                WHEN EXISTS (
                                                    SELECT id
                                                    FROM users
                                                    WHERE id = (SELECT %s)) 
                                                THEN 1
                                                ELSE 0
                                            END''', 
                                            (self.tg_id,))[0]

            if check_id[0] != 0:
                data = conn.fetch_data('''SELECT u.id, firstname, lastname, nickname 
                                        FROM users u
                                        WHERE u.id = %s''', (self.tg_id,))[0]
                return data
            else:
                self.create_profile()

# user = User(tg_id=123456, firstname="Ivan", lastname="Ivanov", tg_nick="ivanivanov")

# user_data = user.fetch_user()
# ic(user_data)
