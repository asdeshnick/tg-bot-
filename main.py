import sqlite3
import telebot

token = 'TOKEH'  # Токен бота взят у @BotFather
bot = telebot.TeleBot(token)

# Функция для подключения к базе данных
def connect_db():
    return sqlite3.connect('users.db')

# Функция для создания таблицы пользователей
def create_users_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            user_group_id INTEGER DEFAULT 2  -- Пользователи по умолчанию не зарегистрированы
        );
        '''
        cursor.execute(create_table_query)

# Функция для получения доступа пользователя
def get_access(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_group_id, user_name FROM users WHERE user_id=?', (user_id,))
        return cursor.fetchone()

# Функция для добавления пользователя в базу данных 
def add_user(user_id, user_name):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (user_id, user_name, user_group_id) VALUES (?, ?, ?)',
                       (user_id, user_name, 0))  # Новые пользователи начинаются с группы '0'
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

def process_name(message):
    user_id = message.chat.id
    user_name = message.text.strip()

    # Добавляем пользователя в базу данных
    add_user(user_id, user_name)

    bot.send_message(message.chat.id, 'Спасибо, {}! Вы успешно зарегистрированы.'.format(user_name))

@bot.message_handler(commands=['admin'])
def handle_admin_command(message):
    access = get_access(message.chat.id)

    if access:
        if access[1] == 1:
            bot.send_message(message.chat.id, 'Привет Admin!')
        elif access[0] == 0:
            bot.send_message(message.chat.id, 'Привет User!')
        else:
            bot.send_message(message.chat.id, 'Неизвестная группа пользователя.')
    else:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы в системе!')

if __name__ == '__main__':
    create_users_table()
    bot.polling(none_stop=True)
