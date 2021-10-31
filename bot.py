import telebot
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

token = config['CREDENTIALS']['token']
bot = telebot.TeleBot(token, parse_mode=None)
