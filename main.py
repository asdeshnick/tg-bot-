import sqlite3
import telebot

token = 'ТОКЕН'

bot = telebot.TeleBot()

# Функция для подключения к базе данных
def connect_db():
    return sqlite3.connect('users.db')

# Функция для получения доступа пользователя
"""
тут мы делаем запрос в базу данных
"""
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
                       (user_id, user_name, '0'))  # Например, что новые пользователи начинаются с группы '0'
        conn.commit()

@bot.message_handler(commands=['start'])   # это сильно умная штука, так что забей на ее, но она нужна
def handle_start_command(message):
    user_id = message.chat.id
    access = get_access(user_id)

# проверка на то что есть ли человек в базе
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


"""
тут кароче важно 
если мы смотрим на id пользователя если он равен 1 то это admin
если он равен 0 то это user
если он равен 2 то челик не зареган 
"""
@bot.message_handler(commands=['admin'])
def handle_admin_command(message):
    print(message.chat.id)
    bot.send_message(message.chat.id, message.text)

    access = get_access(message.chat.id)

    if access:
        if access[0] == '1':
            bot.send_message(message.chat.id, 'Привет Admin!')
        else:
            bot.send_message(message.chat.id, 'Привет User!')
    else:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы в системе!')


#В Python, при выполнении скрипта, этот скрипт получает специальное имя — __main__. 
#Фактически, это означает, что при запуске скрипта из командной строки или при его вызове из другого скрипта,
#Python автоматически присваивает ему имя __main__.
#В то же время, если модуль импортируется в другой скрипт,
#то его имя (__name__) будет равно имени файла (без расширения .py).
#Таким образом, конструкция if __name__ == "__main__": позволяет определить,
#как именно был запущен скрипт — непосредственно или через импорт в другой скрипт.
if __name__ == '__main__':
    bot.polling(none_stop=True)
