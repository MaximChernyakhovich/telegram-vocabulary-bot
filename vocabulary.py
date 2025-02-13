from icecream import ic
from database import Database

class Vocabulary:

    def __init__(self, tg_id: int, words: list = None, word_id: int = None):
        self.tg_id = tg_id
        self.words = words
        self.word_id = word_id

    # Подключение к БД
    def db_connect(self):
        return Database()
    
    def add_words(self):
        db = self.db_connect()
        with db as conn:
            query = """
            SELECT process_user_words(%s, %s::text[])
            """
            words = conn.execute_query(query, (self.tg_id, self.words))
            return words#[0][0]
    
    def delete_words(self):
        db = self.db_connect()
        with db as conn:
            query = """
            SELECT delete_user_words(%s, %s::text[])
            """
            words = conn.execute_query(query, (self.tg_id, self.words))
            return words#[0][0]
    
    def get_user_words(self):
        db = self.db_connect()
        with db as conn:
            query = """
            select uw.word_id, word
            from user_words uw 
            join words_global_test wg on uw.word_id =wg.word_id 
            where uw.user_id = %s
            order by added_at desc

            """
            words = conn.fetch_data(query, (self.tg_id,))
            return words
    
    def get_full_word_info(self):
        db = Database()
        with db as conn:
            query = """
            SELECT word, word_translation, dictionary_api, libre_translate
            FROM words_global_test
            WHERE word_id = %s
            and dictionary_api is not null
            """
            word_info = conn.fetch_data(query, (self.word_id,))
        
        if not word_info:
            return "Информация о слове не найдена."

        word, translation, details, libre_translation = word_info[0]
        result = []

        # Основная информация о слове
        result.append(f"Слово: {word}")
        result.append(f"Перевод: {libre_translation['translatedText'] if len(word) <= 3 else translation}")

        # Проверка details
        if isinstance(details, dict):
            phonetic = details.get("phonetic")
            source_urls = details.get("sourceUrls", [])
            if phonetic:
                result.append(f"Транскрипция: {phonetic}")
            if source_urls:
                result.append(f"Источник: {source_urls[0]}")

            # Определения
            meanings = details.get("meanings", [])
            if meanings:
                result.append("\nОпределения:")
                for meaning in meanings:
                    part_of_speech = meaning.get("partOfSpeech", "Неизвестно").capitalize()
                    result.append(f"  - {part_of_speech}:")
                    for definition in meaning.get("definitions", [])[:3]:
                        example = f" (Пример: {definition['example']})" if "example" in definition else ""
                        result.append(f"    • {definition.get('definition', 'Нет определения')}{example}")

            # Произношение
            phonetics = details.get("phonetics", [])
            if phonetics:
                result.append("\nПроизношение:")
                for phonetic in phonetics:
                    text = phonetic.get("text")
                    audio = phonetic.get("audio")
                    if text or audio:
                        result.append(f"  - {text or 'Нет данных'} (ссылка на аудио: {audio or 'Нет аудио'})")

        # Альтернативные переводы
        if isinstance(libre_translation, dict):
            alternatives = libre_translation.get("alternatives", [])
            if alternatives:
                result.append("\nАльтернативные переводы:")
                for alt in alternatives:
                    result.append(f"  - {alt}")

        return "\n".join(result)

    def get_short_word_info(self):

        db = Database()
        with db as conn:
            query = """
            SELECT word, word_translation, dictionary_api, libre_translate
            FROM words_global_test
            WHERE word_id = %s
            and dictionary_api is not null
            """
            word_info = conn.fetch_data(query, (self.word_id,))
        
        if not word_info:
            return "Информация о слове не найдена."

        word, translation, details, libre_translation = word_info[0]
        result = []

        # Первое определение
        first_meaning = details["meanings"][0] if details["meanings"] else {}
        first_definition = first_meaning["definitions"][0]["definition"] if "definitions" in first_meaning else "Нет данных"
        
        # Короткое описание
        result = f"📖 {word} ({details['phonetic']}) — {libre_translation['translatedText'] if len(word) <= 3 else translation}\n"
        result += f"🔹 {first_definition}\n"
        result += f"🔗 {details['sourceUrls'][0]}"
        
        return result
    
# vc = Vocabulary(tg_id=123, words=[
#     'I', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 
#     'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'])
# ic(vc.add_words())

# vc = Vocabulary(tg_id=123, word_id = 280)
# word = vc.get_short_word_info()
# print(word)