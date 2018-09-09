""" Created by ht.albert on 09/09/2018 """

__author__ = "ht.albert"

import telebot

from config import Config
from .calendar_view import Calendar
import emoji

config = Config()
bot = telebot.TeleBot(config.bot_token)
title = emoji.emojize(':calendar:')


def get_command(callback):
    return callback[0:callback.find(':')]


@bot.message_handler(commands=['start'])
def calendar(mess):
    keyboard = Calendar().create()
    bot.send_message(mess.chat.id, title, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: get_command(call.data) in ['prev', 'next'])
def pagination(call):
    keyboard = Calendar().pagination(call.data)
    bot.edit_message_text(title, call.from_user.id, call.message.message_id, reply_markup=keyboard)
    bot.answer_callback_query(call.id, text="")
