from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Класс, на котором будут все таблицы в БД. Но сам он не таблица"""
    #это поле по умолчанию будет у абсолютно всех строк таблицы, и оно будет ставиться автоматически
    # (на 1 больше чем в прошлой строке)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 