import telebot
import json

# Загрузка данных из JSON-файла
with open('locations.json', 'r', encoding='utf-8') as file:
    locations = json.load(file)

bot = telebot.TeleBot("6905459458:AAHg1WrobA8UuhyZw9NAWEtlzNiQ7hZmnKE")  # Заменить на свой API-токен

@bot.message_handler(commands=['start'])
def start_game(message):
    chat_id = message.chat.id
    # Отправка приветственного сообщения
    bot.send_message(chat_id, "Добро пожаловать в игру 'Выживание на необитаемом острове'!")
    # Отправка описания первой локации и вариантов действий
    send_location(chat_id, "локация0")

@bot.message_handler(func=lambda message: True)
def process_message(message):
    chat_id = message.chat.id
    # Получение выбранного варианта из текста сообщения
    option_text = message.text
    # Поиск локации, связанной с выбранным вариантом
    location_id = find_location_by_option(chat_id, option_text)
    # Если локация найдена, отправка описания и вариантов действий этой локации
    if location_id:
        send_location(chat_id, location_id)
    else:
        # Отправка сообщения об ошибке, если вариант не найден
        bot.send_message(chat_id, "Неправильный выбор, попробуйте еще раз.")

def find_location_by_option(chat_id, option_text):
    # Поиск локации по выбранному варианту действия
    for location_id, location_data in locations.items():
        if 'options' in location_data and option_text in location_data['options']:
            return location_data['options'][option_text]
    return None

def send_location(chat_id, location_id):
    # Отправка описания и вариантов действий локации
    location_data = locations[location_id]
    description = location_data['description']
    options = location_data['options']
    # Генерация списка кнопок для вариантов
    buttons = [telebot.types.KeyboardButton(text=option_text) for option_text in options.keys()]
    # Создание разметки клавиатуры с кнопками
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    # Отправка описания и клавиатуры с вариантами
    bot.send_message(chat_id, description, reply_markup=keyboard)

bot.polling()
