import telebot
import re
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

pattern = re.compile(r'/add[\s]([\w]+)[\s]([\w]+)')

token = config['CREDENTIALS']['token']
bot = telebot.TeleBot(token, parse_mode=None)
