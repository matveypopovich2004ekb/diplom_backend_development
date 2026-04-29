from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from os import getenv

DB_URL = getenv("DATABASE_URL_FOR_PYTHON")

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
    


