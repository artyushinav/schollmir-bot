import telebot
from telebot import types

from function import bot, message_f, message_send, photo_send, next_step, button, callback
from variables import (text1, text2, text3, text4, text5, text6, text7, text8, text9, photo_kalendar, photo_uchetila,
                       monday, tuesday, wednesday, thursday, friday, buffet, raspiss)

@message_f(commands=['start'])
def start(message):
    chat_id = message.chat.id
    file_db_id = open("БД с id пользователей.txt", "a")
    file_db_id.write(str(chat_id) + '\n')
    file_db_id.close()
    file = 'БД с id пользователей.txt'
    uniqlines = set(open(file, 'r', encoding='utf-8').readlines())
    gotovo = open(file, 'w', encoding='utf-8').writelines(set(uniqlines))
    message_send(chat_id, text1)
    next_step(message, clas)
def clas(message):
    chat_id = message.chat.id
    number = str(chat_id) + '-' + str(message.text.strip())
    file_db = open("База Данных.txt", "a")
    file_db.write(number + '\n')
    file_db.close()
    file = 'База Данных.txt'
    uniqlines = set(open(file, 'r', encoding='utf-8').readlines())
    gotovo = open(file, 'w', encoding='utf-8').writelines(set(uniqlines))
    message_send(chat_id, text2)

@message_f(commands=['rasilka'])
def rasilka(message):
    chat_id = message.chat.id
    if chat_id == 1150892740:
        message_send(chat_id, text6)
        next_step(message, send)
    else:
        message_send(chat_id, text7)
def send(message):
    chat_id = message.chat.id
    global message_rasilka
    message_rasilka = message.text.strip()
    buttons = types.InlineKeyboardMarkup(row_width=1)
    button1 = button(text="Пропустить", callback_data='Фотка')
    buttons.add(button1)
    message_send(chat_id, text8, reply_markup=buttons)
    next_step(message, photo_save)
def photo_save(message):
    photo = str(message.photo[-1].file_id)
    for numder in open('БД с id пользователей.txt', 'r').readlines():
        photo_send(numder, photo, f'{message_rasilka}')

@message_f(commands=['raspisanie'])
def raspisanie(message):
    chat_id = message.chat.id
    file_db = open("База Данных.txt", "r")
    x = file_db.readlines()
    for cl in range(len(x)):
        s = [int(i) for i in x[cl].split('-')]
        if s[0] == int(chat_id):
            raspic = s[1]
            break
    photo_send(chat_id, raspiss[int(raspic)-1])

@message_f(commands=['kalendar'])
def kalendar(message):
    chat_id = message.chat.id
    photo_send(chat_id, photo_kalendar)

@message_f(commands=['uchetila'])
def uchetila(message):
    chat_id = message.chat.id
    photo_send(chat_id, photo_uchetila)

@message_f(commands=['pitanie'])
def pitanie(message):
    chat_id = message.chat.id
    buttons = types.InlineKeyboardMarkup(row_width=1)
    button1 = button(text="Меню", callback_data='Меню')
    button2 = button(text="Оставить жалобу", callback_data='Оставить жалобу')
    buttons.add(button1, button2)
    message_send(chat_id, text3, reply_markup=buttons)
def bad_eat(message):
    message_send(1150892740, f'Жалоба: "{message.text.strip()}"')

@callback(func=lambda callback: callback.data)
def check_callback_data(callback):
    chat_id = callback.message.chat.id
    if callback.data == 'Меню':
        buttons = types.InlineKeyboardMarkup(row_width=1)
        button1 = button(text="Понедельник", callback_data='Понедельник')
        button2 = button(text="Вторник", callback_data='Вторник')
        button3 = button(text="Среда", callback_data='Среда')
        button4 = button(text="Четверг", callback_data='Четверг')
        button5 = button(text="Пятница", callback_data='Пятница')
        button6 = button(text="Буфет", callback_data='Буфет')
        buttons.add(button1, button2, button3, button4, button5, button6)
        message_send(chat_id, text4, reply_markup=buttons)
    if callback.data == 'Оставить жалобу':
        message_send(chat_id, text5)
        next_step(callback.message, bad_eat)
    if callback.data == 'Понедельник':
        photo_send(chat_id, monday)
    if callback.data == 'Вторник':
        photo_send(chat_id, tuesday)
    if callback.data == 'Среда':
        photo_send(chat_id, wednesday)
    if callback.data == 'Четверг':
        photo_send(chat_id, thursday)
    if callback.data == 'Пятница':
        photo_send(chat_id, friday)
    if callback.data == 'Буфет':
        photo_send(chat_id, buffet)
    if callback.data == 'Фотка':
        message_send(chat_id, message_rasilka)

bot.polling()