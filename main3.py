import sqlite3
import telebot
from telebot import types
import random

token = '7547484997:AAEEku9A0hWZkhjA3jH4BZd2COyMuVe1BTg'

bot = telebot.TeleBot(token)

# Функция для подключения к базе данных
def connect_db():
    return sqlite3.connect('users.db')

# Функция для создания таблицы users
def create_users_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            user_group_id INTEGER,
            user_name TEXT
        );
        '''
        cursor.execute(create_table_query)

# Функция для получения доступа пользователя
def get_access(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_group_id, user_name FROM users WHERE user_id=?', (user_id,))
        result = cursor.fetchone()
        return result

# Функция для добавления пользователя в базу данных 
def add_user(user_id, user_name):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (user_id, user_name, user_group_id) VALUES (?, ?, ?)',
                       (user_id, user_name, '0'))  # Например, что новые пользователи начинают с группы '0'
        conn.commit()

@bot.message_handler(commands=['start'])
def handle_start_command(message):
    user_id = message.chat.id
    access = get_access(user_id)

    if access:
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы как {}.'.format(access[1])) 
    else:
        msg = bot.send_message(message.chat.id, 'Привет! Пожалуйста, введите ваше имя для регистрации:')
        bot.register_next_step_handler(msg, process_name)

    btn1222 = types.KeyboardButton("👋 Поздороваться")
    # Добавляем кнопки после сообщения
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("проверка на лоха")
    btn2 = types.KeyboardButton("Создавал Андрей")
    markup.add(btn1, btn2, btn1222)
    
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
   
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn11 = types.KeyboardButton('проверка на лоха')
        btn12 = types.KeyboardButton('Создавал Андрей')
        bot.send_message(message.from_user.id, 'мой github ' + '[ссылка](https://github.com/asdeshnick)', parse_mode='Markdown')
        markup.add(btn11, btn12)
        bot.send_message(message.from_user.id, '❓ Выберите ', reply_markup=markup) #ответ бота

    elif message.text == 'проверка на лоха':  
        loh = ["Лох", "Не лоx"]
        loh_bot = random.choice(loh)
        bot.send_message(message.from_user.id, loh_bot, reply_markup=markup) #ответ бота

def process_name(message):
    user_id = message.chat.id
    user_name = message.text.strip()
    print(user_name, user_id)

    # Добавляем пользователя в базу данных
    add_user(user_id, user_name)

    bot.send_message(message.chat.id, 'Спасибо, {}! Вы успешно зарегистрированы.'.format(user_name))

@bot.message_handler(commands=['admin'])
def handle_admin_command(message):
    access = get_access(message.chat.id)

    if access:
        if access[0] == '1':
            bot.send_message(message.chat.id, 'Привет Admin!')
        else:
            bot.send_message(message.chat.id, 'Привет User!')
    else:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы в системе!')

    # Добавляем кнопки для администраторов
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Управление пользователями", callback_data='manage_users')
    btn2 = types.InlineKeyboardButton("Просмотр статистики", callback_data='view_stats')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'manage_users':
        bot.answer_callback_query(call.id, "Вы выбрали управление пользователями.")
        # Логика управления пользователями
    elif call.data == 'view_stats':
        bot.answer_callback_query(call.id, "Вы выбрали просмотр статистики.")
        # Логика просмотра статистики

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
if __name__ == '__main__':
    create_users_table()  # Создаём таблицу перед запуском бота
    bot.polling(none_stop=True)
    