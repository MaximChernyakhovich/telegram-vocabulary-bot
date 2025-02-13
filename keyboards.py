from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import Database
from vocabulary import Vocabulary

# words = [
#     "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew",
#     "kiwi", "lemon", "mango", "nectarine", "orange", "papaya", "quince", "raspberry",
#     "strawberry", "tangerine", "ugli", "viti", "watermelon", "xigua", "yellowfruit", "zucchini",
#     "avocado", "blueberry", "cantaloupe", "dragonfruit", "eggfruit", "feijoa", "grapefruit", "jackfruit",
#     "kumquat", "lime", "melon", "nectar", "olive", "plum", "pear", "pomegranate", "quince",
#     "rhubarb", "soursop", "tamarillo", "ugni", "voavanga", "waxberry", "yam", "ziziphus",
#     "apricot", "blackberry", "coconut", "dates", "elderflower", "figs", "grapefruit", "hibiscus",
#     "italianplum", "jambolan", "kiwifruit", "lemonade", "mangosteen", "orangejuice", "papaw", "pineapple",
#     "santol", "soursap", "tangerines", "waterlemon", "yerba", "zinnia", "acerola", "bromeliad",
#     "cucumber", "dewberry", "elderbloom", "fingerlime", "greenapple", "hass", "icefruit", "jellybean",
#     "kumquats", "lemongrass", "melonball", "nectarines", "oystershell", "pistachio", "quircus", "sambucus",
#     "tamala", "vaselinefruit", "wildberry", "xanthocarpus", "yellowpapaya", "zombfruit", "beetroot", "carrot",
#     "dragonberry", "estragon", "flaxseed", "garlic", "honeycrisp", "indigo", "jujube", "kale", "lemontree"
# ]

class Keyboards:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id
        self.position = 0  # Стартовая позиция пользователя

    # Подключение к БД
    def db_connect(self):
        return Database()
    
    def get_words(self):
        return Vocabulary(tg_id=self.tg_id).get_user_words()

    def get_keyboard(self, index):
        words = [i[1] for i in self.get_words()]
        COLUMNS = 3
        ROWS = 8
        markup = InlineKeyboardMarkup()
        start = index * (COLUMNS * ROWS)
        end = start + (COLUMNS * ROWS)
        page_words = words[start:end]

        #start и end - это индексы слов на текущей странице. Можно использоваться для получения конкретного списка слов из БД, а не всех.
        #print(start, end, page_words)
        
        rows = [page_words[i:i + COLUMNS] for i in range(0, len(page_words), COLUMNS)]

        for row in rows:
            buttons = [InlineKeyboardButton(word, callback_data=f"word_{word}_{index}") for word in row]
            markup.row(*buttons)

        nav_buttons = []
        if index > 0:
            nav_buttons.append(InlineKeyboardButton("⬅", callback_data=f"prev_{index}"))
        if end < len(words):
            nav_buttons.append(InlineKeyboardButton("➡", callback_data=f"next_{index}"))

        if nav_buttons:
            markup.row(*nav_buttons)

        return markup

    def get_word_details_keyboard(self, word, index):
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("Подробнее", callback_data=f"details_{word}_{index}"))
        markup.row(InlineKeyboardButton("⬅ Назад", callback_data=f"back_to_list_{index}"))
        return markup

    def get_word_full_details_keyboard(self, word, index):
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("⬅ Назад", callback_data=f"back_to_word_{index}"))
        return markup

    def update_position(self, new_position):
        self.position = new_position

# d = {}
# for i in kb.get_user_words():
#     d[i[1]] = i[0]

# print(d['santol'])
