import requests
from bs4 import BeautifulSoup as BS
import telebot
from telebot import types
bot = telebot.TeleBot('TOKEN')
"""Keyboard"""
keyboard = types.InlineKeyboardMarkup()
callback_button = types.InlineKeyboardButton(text="Дай мне цитату", callback_data="citaty")
keyboard.add(callback_button)

@bot.message_handler(commands=['start'])
def hi_block(message):
    bot.send_message(message.chat.id, 'Привет')
    bot.send_message(message.chat.id, 'Я бот случайных цитат')
    bot.send_message(message.chat.id, "Хочешь случайную цитату?:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def cit_block(call):
    if call.data == "citaty":
        parser(call)
        bot.send_message(call.from_user.id, "Хочешь случайную цитату?",timeout=2, reply_markup=keyboard)

def parser(call):
    rs = requests.get("https://citaty.info/random")
    root = BS(rs.content, 'html.parser')
    quote, titles, tag = [], [], []
    """Quote"""
    for q in root.select('.even' '.last'):
        quote.append(q.text)
    """Titles"""
    for i in root.select('.even > a'):
        if None not in i.get_attribute_list("title"):
            titles.append(str(*(i.get_attribute_list("title"))) + ": " + i.text)
    """Tags"""
    for n in root.select('.node__topics'):
        tag.append("Ключевые слова: " + n.get_text(separator=", "))

    """Send quote"""
    if quote != []:
        bot.send_message(call.from_user.id, '\n'.join(map(str, quote)))
    if titles != []:
        bot.send_message(call.from_user.id, '\n'.join(map(str, titles)))
    if tag != []:
        bot.send_message(call.from_user.id, '\n'.join(map(str, tag)))

bot.polling(none_stop=True)