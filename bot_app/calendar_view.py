""" Created by ht.albert on 09/09/2018 """

__author__ = "ht.albert"

import calendar
from telebot import types
import emoji
import datetime as dt


class Calendar:
    WEEK_DAYS = calendar.weekheader(2).split(' ')

    def __init__(self):
        self.today = dt.datetime.today()

    def create(self, year=None, month=None):
        """ generate calendar for telegram message """
        if not all([year, month]):
            year, month = self.today.year, self.today.month

        markup = types.InlineKeyboardMarkup()

        row = list()
        row.append(types.InlineKeyboardButton(calendar.month_name[month] + " " + str(year), callback_data="ignore"))
        markup.row(*row)

        row = []
        for day in self.WEEK_DAYS:
            row.append(types.InlineKeyboardButton(day, callback_data="ignore"))
        markup.row(*row)

        my_calendar = calendar.monthcalendar(year, month)
        for week in my_calendar:
            row = []
            for day in week:
                item = types.InlineKeyboardButton(" ", callback_data="ignore") if day == 0 \
                    else types.InlineKeyboardButton(self.__get_day(day, month, year),
                                                    callback_data="day_info:{}-{}-{}".format(year, month, day))
                row.append(item)
            markup.row(*row)

        row = list()
        row.append(types.InlineKeyboardButton("<", callback_data="prev:{}-{}-{}".format(year, month, 0)))
        row.append(types.InlineKeyboardButton("Menu", callback_data="ignore"))
        row.append(types.InlineKeyboardButton(">", callback_data="next:{}-{}-{}".format(year, month, 0)))
        markup.row(*row)

        return markup

    def pagination(self, command):
        year, mouth, day = self.get_day_from_commands(command)
        markup = self.__next_month(year, mouth) if command[0:4] == 'next' else self.__prev_month(year, mouth)
        return markup

    def __next_month(self, year, month):
        """ generate next month calendar """
        year, month = (year, month + 1) if month < 12 else (year + 1, 1)

        return self.create(year, month)

    def __prev_month(self, year, month):
        """ generate prev month calendar """
        year, month = (year, month - 1) if month > 1 else (year - 1, 12)

        return self.create(year, month)

    @staticmethod
    def get_day_from_commands(command):
        """ day from command / commands format name:year-month-day """
        year, mouth, day = (int(_) for _ in command[command.find(':')+1:].split('-'))
        return year, mouth, day

    def __get_day(self, day, month, year):
        """ return emoji if current day """
        date = self.today.today().replace(day=day, month=month, year=year).date()
        if self.today.date() == date:
            i, j = divmod(day, 10)
            # emoji format for current date
            ret = (emoji.emojize(':keycap_{}:'.format(i)) if i else '') + emoji.emojize(':keycap_{}:'.format(j))
            return ret

        return str(day)
