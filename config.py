import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN')

CHAT_ADMIN  = os.getenv('CHAT_ADMIN')