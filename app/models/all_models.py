from app.models.basic_model import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime, timezone

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
    amount: Mapped[float]  


class OrdersORM(Base):
    """Модель таблицы со списокм заказов"""

    __tablename__ = "orders"

    created_at: Mapped[datetime] = mapped_column(
        default = lambda: datetime.now(timezone.utc) # по умолчанию при создании заказа 
        # будет присваиватся время создания с учетом временной зоны

        )

class OrderItemORM(Base):
    """Модель таблицы с параметрами заказа"""

    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"), nullable=False)

    quantity: Mapped[int]










