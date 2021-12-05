import os

from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    return (f'postgresql://'
            f'{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@'
            f'{os.environ.get("DB_HOST")}/{os.environ.get("DB_NAME")}')
