import telebot
from telebot import types


def add_one_to_event(line):
    ls = line.replace("[", "").replace("]", "").replace("'", "").replace(", ", ",").split(",")
    ls[-1] = str(int(ls[-1]) + 1)
    return str(ls)

name = ''
date = ''
place = ''
description = ''


# bot = telebot.TeleBot("1002707245:AAHIrGUNPOcLvb2ygCUJGRaXtC1Ho4nqJu0")

bot = telebot.TeleBot("1015104677:AAF5KzY8WEENOwDBXceKk7BLJ9k3npUtm5o")

@bot.message_handler(content_types = ['text'])
def send_echo(message):
    start_buttons = types.ReplyKeyboardMarkup()
    add_but = types.KeyboardButton('Add event')
    see_but = types.KeyboardButton('List of events')
    start_buttons.row(add_but, see_but)
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Hello, I'm event bot😄! To create an event, press 'Add event'\nTo see some events, press 'List of events'😜", reply_markup=start_buttons)

    if message.text == 'Add event':
        bot.send_message(message.from_user.id, "Enter the name of your event")
        bot.register_next_step_handler(message, get_name)
    if message.text == 'List of events':
         bot.send_message(message.chat.id, see(message))

@bot.message_handler(commands = ['add_event'])
def get_name(message): 
    global user
    global organizator
    global name
    organizator = "@" + message.from_user.username
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name

    try:
        user = user_name + " " +  user_surname + " " + "@" + message.from_user.username
    except:
        try:
            user = user_name + " " + "@" + message.from_user.username
        except:
            user = user_name

    name = message.text
    bot.send_message(message.from_user.id, 'Enter date and time')
    bot.register_next_step_handler(message, get_date)


def get_date(message):
    global date
    date = message.text
    bot.send_message(message.from_user.id, 'Where event will take place?')
    bot.register_next_step_handler(message, get_place)


def get_place(message):
    global place
    place = message.text
    bot.send_message(message.from_user.id, 'Description/links')
    bot.register_next_step_handler(message, get_desc)


def get_desc(message):
    global description
    description = message.text
    bot.send_message(message.from_user.id, "Event is created ✅")
    Events = [name, date, place, description, user, '1']
    print(Events)
    with open('events.txt', 'a', encoding=' utf-8 ') as file:
        file.write(str(Events)+"\n")


# prints events.txt
@bot.message_handler(commands=['see_events'])
def see(message):
    num_line = 0
    
    with open('events.txt', 'r', encoding=' utf-8 ') as file:
        for line in file:
            line = line.strip()
            line = line.split(",")
            print(line)
            output = ("Event name: " + str(line[0])[1:] + "\n" 
                      "📅date/time: "+ line[1] + "\n" + 
                      "🌄place: " + line[2] + "\n" +
                      "📄description: " + line[3] + "\n" + 
                      "👤Creator: " + line[4] + "\n" + 
                      "👨‍👨‍👧‍👦Visitors: " + line[5][:-1])
            key = types.InlineKeyboardMarkup()
            key.add(types.InlineKeyboardButton("+", callback_data = str(num_line)))
            key.add(types.InlineKeyboardButton("🔴Для Ігарька", callback_data = str(num_line)+ " "))
            bot.send_message(message.from_user.id, output, reply_markup=key)
            num_line += 1
            global userka
            userka = message
            
# add one when user presses +
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    num_line = 0
    lines = []
    with open('events.txt', 'r', encoding=' utf-8 ') as file:
        for line in file:
            lines.append(line)
    with open('events.txt', 'w', encoding=' utf-8 ') as file:
        for line in lines:
            line = line.strip()
            if str(num_line) == call.data:
                line = add_one_to_event(line)
            file.write(str(line)+"\n")
            num_line += 1


bot.polling(none_stop = True)