""" Created by ht.albert on 09/09/2018 """

__author__ = "ht.albert"

import telebot

from config import Config
from .calendar_view import Calendar, DayView
import emoji

config = Config()
bot = telebot.TeleBot(config.bot_token)
title = 'Your Calendar ' + emoji.emojize(':calendar:')


def get_command(callback):
    return callback[0:callback.find(':')]


def get_day_from_commands(command):
    """ day from command / commands format name:year-month-day """
    year, mouth, day = (int(_) for _ in command[command.find(':')+1:].split('-'))
    return year, mouth, day


@bot.message_handler(commands=['start'])
def calendar(mess):
    keyboard = Calendar().create()
    bot.send_message(mess.chat.id, title, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: get_command(call.data) in ['prev', 'next'])
def pagination(call):
    keyboard = Calendar().pagination(call.data)
    bot.edit_message_text(title, call.from_user.id, call.message.message_id, reply_markup=keyboard)
    bot.answer_callback_query(call.id, text="")


@bot.callback_query_handler(func=lambda call: get_command(call.data) == 'day')
def day_info(call):
    y, m, d = get_day_from_commands(call.data)
    date_obj = DayView(y, m, d)
    keyboard = date_obj.footer
    bot.edit_message_text(
        date_obj.title, call.from_user.id, call.message.message_id, reply_markup=keyboard,
    )
    bot.answer_callback_query(call.id, text="")


@bot.callback_query_handler(func=lambda call: get_command(call.data) == 'call')
def calendar_with_day(call):
    y, m, d = get_day_from_commands(call.data)
    keyboard = Calendar().create(year=y, month=m)
    bot.edit_message_text(
        title, call.from_user.id, call.message.message_id, reply_markup=keyboard,
    )
    bot.answer_callback_query(call.id, text="")
