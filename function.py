from TOKEN import TOKEN
import telebot
from telebot import types

bot = telebot.TeleBot(TOKEN)

message_send = bot.send_message
photo_send = bot.send_photo

message_f = bot.message_handler
next_step = bot.register_next_step_handler
callback = bot.callback_query_handler

button = types.InlineKeyboardButton