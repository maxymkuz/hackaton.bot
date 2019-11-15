import telebot
from telebot import types


bot = telebot.TeleBot("1055491905:AAE7lgq_WIPI_wPZzbdJluf29Tc1sX024LY")
@bot.message_handler(content_types = ['text'])
def send_echo(message):
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('Додати івент')
    itembtnv = types.KeyboardButton('Подивитися івенти')
    markup.row(itembtna, itembtnv)
    if message.text == '/start':
        bot.send_message(message.chat.id, "Choose", reply_markup=markup)
    if message.text == 'Додати івент':
        bot.send_message(message.chat.id, "Enter a name for your event", reply_markup=markup)
    if message.text == 'Подивитися івенти':
        f = open("events.txt", "r", encoding="utf-8")
        evets = f.readlines()
        
        f.close()
    
    
bot.polling( none_stop = True )