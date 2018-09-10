""" Created by ht.albert on 09/09/2018 """

__author__ = "ht.albert"

import os

import yaml

DEF_CONFIG = 'config.yml'


def get_from_env_or_config(config, param, default=None):
    return os.environ.get(param.upper()) or config.get(param, default)


class Config:
    """ init configurations """

    config_file = DEF_CONFIG
    bot_token = None
    host = None
    port = None
    proxy = None
    is_local = None

    def __init__(self, config_file=None):
        if not Config.bot_token:
            self.load(config_file)

    @staticmethod
    def load(config_file):
        if config_file:
            Config.config_file = config_file

        with open(Config.config_file, 'r') as c:
            config = yaml.load(c)

        Config.bot_token = get_from_env_or_config(config, 'bot_token')
        Config.port = get_from_env_or_config(config, 'port', 5000)
        Config.host = get_from_env_or_config(config, 'host')
        Config.proxy = get_from_env_or_config(config, 'proxy')
        Config.is_local = True if Config.host == 'localhost' else False
