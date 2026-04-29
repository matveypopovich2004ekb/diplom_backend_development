from app.models.basic_model import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class ProductORM(Base):
    """Модель табицы с запасом продуктов"""

    __tablename__ = "products"

    name: Mapped[str]
    unit: Mapped[str] #в чем измеряется количество товара
    quantity: Mapped[float] # количтсво товара
    critical_quantity: Mapped[float] # количество, когданадо делать новый закуп


class MenuORM(Base):
    """Модель табицы с Меню"""

    __tablename__ = "menu_items"

    name: Mapped[str] #название блюда
    

class MenuItemIngredientORM(Base):
    """Модель табицы с запасом продуктов"""

    __tablename__ = "menu_item_ingredients"

    #ай ди соответствующего товара из меню
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"), nullable=False) 
    #ай ди соответствующего продукта  из меню
    product_id: Mapped[int]  = mapped_column(ForeignKey("products.id"), nullable=False)
    amount: Mapped[float] # количтсво продутка в блюде
