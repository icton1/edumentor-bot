import os
import sys
import telebot
from os.path import dirname, join, abspath
from dotenv import load_dotenv
load_dotenv()
sys.path.insert(0, abspath(dirname(__file__)))

TOKEN = os.environ.get('TG_TOKEN')
SHELVE_NAME = "shelve.db"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

bot = telebot.TeleBot(TOKEN)


def get_filename(relative_path):
    return os.path.join(ROOT_DIR, relative_path)
