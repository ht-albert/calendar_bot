""" Created by ht.albert on 09/09/2018 """

__author__ = "ht.albert"


import time
from flask import Flask, request
import telebot
from config import Config

config = Config()

telebot.apihelper.proxy = {
    'https': config.proxy
}

app = Flask(__name__)

bot = telebot.TeleBot(config.bot_token)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(mess):
    bot.send_message(mess.chat.id, "Hello world!")


@app.route('/' + config.bot_token, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return ''


if __name__ == '__main__':
    if config.is_local:
        bot.polling()
    else:
        bot.set_webhook(url=config.host + config.bot_token)
        time.sleep(0.1)
        app.run(host=config.host, port=config.port, debug=True)
