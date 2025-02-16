from keyboards import Keyboards
from vocabulary import Vocabulary

class VocabularyHandler:
    def __init__(self, bot):
        self.bot = bot
        self.register_handlers()

    def handle_inline_callback(self, call):
        """Обработка инлайн-кнопок словаря"""
        if call.data.startswith("prev") or call.data.startswith("next"):
            self.callback_query(call)
        elif call.data.startswith("word_"):
            self.show_word_details(call)
        elif call.data.startswith("details_"):
            self.show_word_full_details(call)
        elif call.data.startswith("back_to_word_"):
            self.go_back_to_word(call)
        elif call.data.startswith("back_to_list_"):
            self.go_back(call)
    
    def get_words(self, message):
        #return Keyboards(message.chat.id).get_words()
        k = Keyboards(message.chat.id).get_words()
        return {i[1]: i[0] for i in k}
    
    def get_short_info(self, message, word_id):
        return Vocabulary(tg_id=message.chat.id, word_id=word_id).get_short_word_info()
    
    def get_full_info(self, message, word_id):
        return Vocabulary(tg_id=message.chat.id, word_id=word_id).get_full_word_info()

    def send_word_list(self, message):
        chat_id = message.chat.id
        keyboard = Keyboards(chat_id)
        self.bot.send_message(chat_id, "Выберите слово:", reply_markup=keyboard.get_keyboard(0))
    
    def callback_query(self, call):
        words = [i[1] for i in self.get_words(call.message)]
        
        chat_id = call.message.chat.id
        current_index = int(call.data.split("_")[1])
        
        if "prev" in call.data and current_index > 0:
            new_index = current_index - 1
        elif "next" in call.data and (new_index := current_index + 1) * (3 * 8) < len(words):
            pass
        else:
            return
        
        keyboard = Keyboards(chat_id)
        keyboard.update_position(new_index)
        self.bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, 
                                   text="Выберите слово:", reply_markup=keyboard.get_keyboard(new_index))
    
    def show_word_details(self, call):
        _, word, index = call.data.split("_")
        self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                   text=f"Описание слова:\n\n{self.get_short_info(call.message, self.get_words(call.message)[word])}", 
                                   reply_markup=Keyboards(call.message.chat.id).get_word_details_keyboard(word, index))
    
    def show_word_full_details(self, call):
        _, word, index = call.data.split("_")
        self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                   text=f"Полное описание слова:\n\n{self.get_full_info(call.message, self.get_words(call.message)[word])}", 
                                   reply_markup=Keyboards(call.message.chat.id).get_word_full_details_keyboard(word, index))
    
    def go_back_to_word(self, call):
        index = int(call.data.split("_")[-1])
        self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                   text="Выберите слово:", reply_markup=Keyboards(call.message.chat.id).get_keyboard(index))
    
    def go_back(self, call):
        index = int(call.data.split("_")[3])
        self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                   text="Выберите слово:", reply_markup=Keyboards(call.message.chat.id).get_keyboard(index))
    
    def register_handlers(self):
        self.bot.message_handler(commands=["vocabulary"])(self.send_word_list)
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("prev") or call.data.startswith("next"))(self.callback_query)
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("word_"))(self.show_word_details)
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("details_"))(self.show_word_full_details)
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("back_to_word_"))(self.go_back_to_word)
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("back_to_list_"))(self.go_back)