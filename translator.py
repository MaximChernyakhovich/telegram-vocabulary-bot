import requests

class Translator:
    def __init__(self):
        self.url = "https://translate.googleapis.com/translate_a/single"
        self.params = {
            "client": "gtx",
            "dt": "t"  # Запрос на текстовый перевод
        }

    def _send_request(self, word, source_lang, target_lang):
        """
        Общий метод для отправки запросов к Google Translate.
        """
        self.params["sl"] = source_lang
        self.params["tl"] = target_lang
        self.params["q"] = word

        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code, response.text)
            return None

    def detect_language(self, word):
        """
        Определяет язык исходного текста с помощью Google Translate.
        """
        response = self._send_request(word, "auto", "en")
        if response:
            detected_language = response[-1][0][0]
            return detected_language
        return None

    def translate(self, word):
        """
        Переводит слово с английского на русский или с русского на английский.
        """
        detected_language = self.detect_language(word)
        if not detected_language:
            return None

        # Определяем язык перевода
        target_lang = "en" if detected_language == "ru" else "ru"

        response = self._send_request(word, detected_language, target_lang)
        if response:
            translated_text = response[0][0][0]
            return translated_text
        return None

translator = Translator()
word = "apple"
translated_word = translator.translate(word)
print(f"Перевод: '{word}': {translated_word}")