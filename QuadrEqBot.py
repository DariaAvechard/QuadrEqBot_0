# -*- coding: utf-8 -*-
import telebot
import time
import numpy as np
from telebot import types

bot = telebot.TeleBot('bot_token')

@bot.message_handler(commands = ['start'])
def start(message):
    sent = bot.send_message(message.chat.id, 'Как Вас зовут?')
    bot.register_next_step_handler(sent, hello)

def hello(message):
    bot.send_message(message.chat.id, 'Здравствуйте, {name}. Рад Вас видеть.'.format(name = message.text))
    keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = 'Решить уравнение'))
    sent = bot.send_message(message.chat.id, 'Я могу помочь Вам решить квадратное уравнение.', reply_markup = keyboard)
    bot.register_next_step_handler(sent, q0)

@bot.message_handler(commands = ['helpme'])
def question(message):
    keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = 'Решить уравнение'))
    sent = bot.send_message(message.chat.id, 'Решить другое уравнение?', reply_markup = keyboard)
    bot.register_next_step_handler(sent, q0)

def isNotEmpty(s):
    return bool(s and s.strip())

def q0(message):
    global a0
    a0 = bot.send_message(message.chat.id, 'Введите a')
    bot.register_next_step_handler(a0, q1)

def q1(message):
    global a
    a = message.text
    if (isNotEmpty(a) == True and a.lstrip('-').isdigit() == True):
        global b0
        b0 = bot.send_message(message.chat.id, 'Введите b')
        bot.register_next_step_handler(b0, q2)
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
        keyboard.add(types.KeyboardButton(text = 'Повторить ввод'))
        sent = bot.send_message(message.chat.id, 'Не числовое значение', reply_markup = keyboard)
        bot.register_next_step_handler(sent, q0)

def q2(message):
    global b
    b = message.text
    if (isNotEmpty(b) == True and b.lstrip('-').isdigit() == True):
        global c0
        c0 = bot.send_message(message.chat.id, 'Введите c')
        bot.register_next_step_handler(c0, q3)
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
        keyboard.add(types.KeyboardButton(text = 'Повторить ввод'))
        sent = bot.send_message(message.chat.id, 'Не числовое значение', reply_markup = keyboard)
        bot.register_next_step_handler(sent, q0)
def q3(message):
    c = message.text
    if (isNotEmpty(c) == True and c.lstrip('-').isdigit() == True):
        keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
        keyboard.add(types.KeyboardButton(text = 'Спасибо!'))
        if int(a) == 0:
            sent = bot.send_message(message.chat.id, 'Не квадратное уравнение', reply_markup = keyboard)
        else:
            res = quadr_eq(int(a), int(b), int(c))
            if (res[0].imag == 0 and res[1].imag == 0):
                s11 = str(res[0].real)
                s12 = str(res[1].real)
                sent = bot.send_message(message.chat.id, 'x1 = {s11}, '.format(s11 = str(s11)) + 'x2 = {s12}'.format(s12 = str(s12)), reply_markup = keyboard)
            else:
                s21 = str(res[0])
                s22 = str(res[1])
                sent = bot.send_message(message.chat.id, 'x1 = {s21}, '.format(s21 = str(s21)) + 'x2 = {s22}'.format(s22 = str(s22)), reply_markup = keyboard)
        bot.register_next_step_handler(sent, question)
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
        keyboard.add(types.KeyboardButton(text = 'Повторить ввод'))
        sent = bot.send_message(message.chat.id, 'Не числовое значение', reply_markup = keyboard)
        bot.register_next_step_handler(sent, q0)

def quadr_eq(a1, b1, c1):
    if a1 == 0:
        return 0
    else:
        D = b1 ** 2 - 4 * a1 * c1
        x1 = (-b1 - np.sqrt(complex(D))) / (2 * a1)
        x2 = (-b1 + np.sqrt(complex(D))) / (2 * a1)
        return x1, x2

while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(10)
