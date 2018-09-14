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
                                                    callback_data="day:{}-{}-{}".format(year, month, day))
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
        ret = str()
        if self.today.date() == date:
            # emoji format for current date
            ret = emoji.emojize(':round_pushpin:')

        return ret + str(day)


class DayView(object):

    def __init__(self, year, month, day):
        self.day = day
        self.month = month
        self.year = year
        self.date = dt.datetime.today().date().replace(day=day, month=month, year=year)

    @property
    def title(self):
        return 'Информация на {}/{}/{}'.format(self.day, self.month, self.year)

    def __callback_day(self, next_day):
        date = self.date + dt.timedelta(days=1) if next_day else self.date - dt.timedelta(days=1)
        return 'day:{year}-{month}-{day}'.format(year=date.year, month=date.month, day=date.day)

    @property
    def footer(self):
        markup = types.InlineKeyboardMarkup()
        row = list()
        row.append(types.InlineKeyboardButton('<', callback_data=self.__callback_day(False)))
        row.append(types.InlineKeyboardButton('Calendar',
                                              callback_data="call:{}-{}-{}".format(self.year, self.month, self.day)))
        row.append(types.InlineKeyboardButton('>', callback_data=self.__callback_day(True)))
        markup.row(*row)
        return markup
