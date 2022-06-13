from email import message
import telebot
from telebot import types

name    = ""
surname = ""
age     = 0
bot = telebot.TeleBot("your_key")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "пришли: \nПривет")

@bot.message_handler(func=lambda message: True)
def ehco_add(message):
    if message.text == "Привет":
        bot.reply_to(message, 'Для регистрации введи: /reg')
    elif message.text == "/reg":
        bot.send_message(message.from_user.id, "Как твое имя?")
        bot.register_next_step_handler(message,reg_name)

def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id,"Какая у тебя Фамилия?")
    bot.register_next_step_handler(message,reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id,"Ваш Возраст?")
    bot.register_next_step_handler(message,reg_age)

def reg_age(message):
    global age
    age = message.text 
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Вводите цифрами!" )
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Ваш возраст ' + str(age) + ' И Вас зовут: ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text = question, reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id,"Приятно Познакомится! Идет Запись в БД!")
        upfile= name+' '+surname+" .txt"
        f = open(upfile, 'w')
        f.write("\nName: "+name)
        f.write("\nSurname: "+surname)
        f.write("\nAge :"+age)
        f.close()
        bot.send_message(call.message.chat.id, "Вы успешно прошли регистрацию" )  
        bot.register_next_step_handler(call.message, stopet)  
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Попробуем еще раз!")
        bot.send_message(call.message.chat.id, "Привет! Давай познакомимся! Как тебя зовут?")
        bot.register_next_step_handler(call.message, reg_name)

def stopet(message):
    bot.send_message(message.chat.id, "На этом пока все!\n Спасибо за участие!")

bot.infinity_polling()
