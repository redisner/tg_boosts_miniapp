from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_NAME = getenv('DB_NAME')

api_id = int(getenv('USERBOT_API_ID'))
api_hash = getenv('USERBOT_API_HASH')

BOT_TOKEN = getenv("BOT_TOKEN")
