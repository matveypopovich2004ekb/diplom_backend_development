from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from dotenv import load_dotenv
from os import getenv


load_dotenv() # теперь getenv сможет прочитать .env

DB_URL = getenv("DATABASE_URL_FOR_PYTHON") #берем адрес БДдля подключения в  .env

# устанавливаем связь с БД и содаем сессион
engine = create_engine(DB_URL)
session_local_class = sessionmaker(bind=engine)

def get_database():
    """эта функция выдает сессию и заерывает ее после того, как отработает эндпоинт"""
    db_session = session_local_class()

    try:
        yield db_session
    finally:
        db_session.close()
    


