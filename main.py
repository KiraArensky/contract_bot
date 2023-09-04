import sqlite3
from os import system
import time
import traceback

try:
    import requests
    import telebot
except ModuleNotFoundError:
    system("pip install pyTelegramBotAPI")
    system("pip install requests")
    import requests
    import telebot

from telebot import types
from posts import *

bot = telebot.TeleBot('')  # токен бота из BotFather

print('run')


@bot.message_handler(commands=['start'])  # запуск бота
def start(message):
    con = sqlite3.connect("database/chats.db")
    cur = con.cursor()

    result = cur.execute("""SELECT id FROM id""").fetchall()
    id_list = [elem[0] for elem in result]

    chatid = message.chat.id  # переменная для сохранения айди чата
    print(message.from_user.first_name, chatid, f'tg://user?id={chatid}')  # имя и айди чата отправителя

    if chatid not in id_list:
        cur.execute(
            f'''INSERT INTO id (id, key) VALUES({chatid}, 'defolt') ''')
        con.commit()

    markup = types.InlineKeyboardMarkup()  # cоздание inline кнопок
    btn1 = types.InlineKeyboardButton("Нефтеюганский район", callback_data='nefteyugansk')
    btn2 = types.InlineKeyboardButton("Другая территория", callback_data='other')
    markup.row(btn1, btn2)

    msg = bot.send_message(chatid, text="Привет, откуда ты?", reply_markup=markup)
    cur.execute(
        f'''UPDATE id SET back = {msg.id} WHERE id = {message.chat.id} ''')
    con.commit()


@bot.message_handler(commands=['menu'])  # запуск бота
def menu(message):
    con = sqlite3.connect("database/chats.db")
    cur = con.cursor()

    back = cur.execute(f'''SELECT back FROM id WHERE id = {message.chat.id}''').fetchone()[0]
    try:
        bot.delete_message(message.chat.id, back)
    except telebot.apihelper.ApiTelegramException:
        pass

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Как поступить на военную службу")
    btn2 = types.KeyboardButton("Меры соцподдержки")
    btn3 = types.KeyboardButton("Сменить регион")
    markup.add(btn1)
    markup.row(btn2, btn3)

    msg = bot.send_message(message.chat.id, text="Выбери, что тебе интересно узнать в меню", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message, text=None):
    con = sqlite3.connect("database/chats.db")
    cur = con.cursor()

    back = cur.execute(f'''SELECT back FROM id WHERE id = {message.chat.id}''').fetchone()[0]
    menu_msg = cur.execute(f'''SELECT menu_msg FROM id WHERE id = {message.chat.id}''').fetchone()[0]
    try:
        if text is None:
            bot.delete_message(message.chat.id, menu_msg)
        bot.delete_message(message.chat.id, back)
    except telebot.apihelper.ApiTelegramException:
        pass

    if text:
        txt = text
    else:
        txt = message.text

        cur.execute(
            f'''UPDATE id SET menu_msg = {message.id} WHERE id = {message.chat.id} ''')
        con.commit()

    if txt == "Меры соцподдержки":
        support(bot, message, cur, con)
    elif txt == "Как поступить на военную службу":
        how_join(bot, message, cur, con)
    elif txt == "Сменить регион":
        start(message)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    con = sqlite3.connect("database/chats.db")
    cur = con.cursor()

    if call.message:
        if call.data == "nefteyugansk":
            cur.execute(
                f'''UPDATE id SET city = "Nefteyugansk" WHERE id = {call.message.chat.id} ''')
            con.commit()
            menu(call.message)
        elif call.data == "other":
            cur.execute(
                f'''UPDATE id SET city = "other" WHERE id = {call.message.chat.id} ''')
            con.commit()
            menu(call.message)
        elif call.data[:3] == "sup":
            back = cur.execute(f'''SELECT back FROM id WHERE id = {call.message.chat.id}''').fetchone()[0]
            try:
                bot.delete_message(call.message.chat.id, back)
            except telebot.apihelper.ApiTelegramException:
                pass

            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Назад", callback_data='back')
            markup.row(btn1)
            with open(f'database/posts/{call.data}.txt') as post_txt:
                msg = bot.send_message(call.message.chat.id,
                                       text=f'{post_txt.readlines()[0]}', reply_markup=markup)
                cur.execute(
                    f'''UPDATE id SET back = {msg.id} WHERE id = {call.message.chat.id} ''')
                con.commit()

        elif call.data == "back":
            text = 'Меры соцподдержки'
            func(call.message, text)


def telegram_polling():
    try:
        bot.polling()
    except requests.exceptions.ReadTimeout:
        bot.send_message(-633607298, text="restart bot")
        traceback_error_string = traceback.format_exc()
        with open("Error.Log", "a") as myfile:
            myfile.write("\r\n\r\n" + time.strftime("%c") + "\r\n<<ERROR polling>>\r\n" + traceback_error_string
                         + "\r\n<<ERROR polling>>")
        bot.stop_polling()
        time.sleep(10)
        telegram_polling()


if __name__ == '__main__':
    telegram_polling()