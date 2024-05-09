import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')