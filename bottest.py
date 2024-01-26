import telebot
import json

# загружаем данные о прогрессе пользователя из json-файла
with open("progress.json", "r") as file:
    progress = json.load(file)

# записываем прогресс пользователя в файл
def save_progress(chat_id, question):
    if chat_id not in progress:
        progress[chat_id] = {}
    progress[chat_id]["question"] = question

    with open("progress.json", "w") as file:
        json.dump(progress, file)

# получаем прогресс пользователя из файла
def get_progress(chat_id):
    if chat_id in progress:
        return progress[chat_id]["question"]
    else:
        return None

# удаляем прогресс пользователя из файла
def delete_progress(chat_id):
    if chat_id in progress:
        del progress[chat_id]

    with open("progress.json", "w") as file:
        json.dump(progress, file)

# загружаем данные о локациях из json-файла
with open('locations.json', 'r', encoding='utf-8') as file:
    locations = json.load(file)

# создаем экземпляр бота
bot = telebot.TeleBot('6905459458:AAHg1WrobA8UuhyZw9NAWEtlzNiQ7hZmnKE')

# словарь, в котором будем хранить текущие локации игроков
players = {}

@bot.message_handler(commands=['start'])
def start_game(message):
    chat_id = message.chat.id
    # отправка приветственного сообщения
    bot.send_message(chat_id, "добро пожаловать в игру 'выживание на необитаемом острове'!")
# создаем нового игрока и начинаем игру с первой локации
    players[chat_id] = {'current_location': 'локация0'}
    show_location(chat_id)

# обработчик для кнопок с вариантами ответа игрока
@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    chat_id = call.message.chat.id

    # обрабатываем выбор игрока
    player = players[chat_id]
    player['current_location'] = call.data

    # отображаем новую локацию
    show_location(chat_id)

# функция для отображения текущей локации
def show_location(chat_id):
    player = players[chat_id]
    location = locations[player['current_location']]
    with open(location['photo'], 'rb') as photo_file:
        bot.send_photo(chat_id, photo_file, caption=location['description'])

    # отправляем сообщение с описанием локации
    bot.send_message(chat_id, location['description'])

    # создаем inline-клавиатуру с кнопками для выбора действия
    keyboard = telebot.types.InlineKeyboardMarkup()
    for option, destination in location['options'].items():
        button = telebot.types.InlineKeyboardButton(text=option, callback_data=destination)
        keyboard.add(button)

    bot.send_message(chat_id, "Если хотите начать квест заново нажмите кнопку /start "
                              "Выберите действие:", reply_markup=keyboard)

# запускаем бота
bot.polling()
