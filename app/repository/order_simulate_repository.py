from app.models.all_models import ProductORM, MenuORM, MenuItemIngredientORM, OrderItemORM, OrdersORM

from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence


class ProductRepository():
    """тут прописано взаимодействие Products с БД"""

    def __init__(self, db: Session):
        self.db = db

    def get_list(self) -> Sequence[ProductORM]:
        """выдает полный список продуктов из БД"""
        sequence_of_products = self.db.scalars(select(ProductORM)).all()
        return sequence_of_products
    
    def get_ids_list(self) -> Sequence[int]:
        """возвращает список всех ID в таблице продуктов(нужен для того, чтобы проверять, есть ли указанный 
        ингредиент в списке продуктов при добавлении Элемента Меню(блюда)- если непонятно см. class MenuService())"""
        id_list = self.db.scalars(select(ProductORM.id)).all()

        return id_list
    
    def get_by_id(self, product_id: int) -> ProductORM | None:
        """Просто по идентификатору продукта получаем его строку из таблицы ProductORM"""
        product = self.db.get(ProductORM, product_id)

        return product
    
    def create(self, product_atributes: dict) -> ProductORM:
        """Создает новый продукт"""

        new_product = ProductORM(**product_atributes)
        self.db.add(new_product)
        return new_product

       
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

class MenuRepository():
    """тут прописано взаимодействие Menu с БД"""

    def __init__(self, db: Session):
        self.db = db

    def get_list(self) -> Sequence[MenuORM]:
        """выдает список блюд из Меню"""

        sequence_of_menu_item = self.db.scalars(select(MenuORM)).all()
        return sequence_of_menu_item
    
    def create_menu_item(self, name: str):
        """создает блюда в таблице MenuORM"""

        new_menu_item = MenuORM(name=name)
        self.db.add(new_menu_item)

        return new_menu_item
    
    def create_ingredient_for_menu_item(self,
                                         menu_item_id: int,
                                         product_id: int,
                                         amount: int
                                         ):
        """добавляем ингредиент к только что созданному элементу меню в MenuItemIngredientORM"""

        new_ingredient = MenuItemIngredientORM(
            menu_item_id=menu_item_id, product_id=product_id, amount=amount
        )
        self.db.add(new_ingredient) 

        return new_ingredient
        


    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


class SimulateOrderRepository():
    """тут прописано взаимодействие Menu с БД"""

    def __init__(self, db: Session):
        self.db = db

    def MenuItemIngredientORM_from_menu_item_id(
            self, 
            menu_item_id: int
            ) -> Sequence[MenuItemIngredientORM]:
        """метод возвращает все строки из MenuItemIngredientORM с указанным в параметрах id"""


        ingredients_sequence = self.db.query(MenuItemIngredientORM).filter(
            MenuItemIngredientORM.menu_item_id == menu_item_id
        ).all()

        return ingredients_sequence
    
    def create_new_order(self):
        """создает заказ в БД"""

        new_order = OrdersORM()
        self.db.add(new_order)
        
        return new_order # возвращаем заказ

    def create_new_order_item(self, order_id, menu_item_id, quantity):
        """создает новый объект в OrderItemORM"""
        order_item = OrderItemORM(order_id=order_id, 
                                 menu_item_id=menu_item_id, 
                                 quantity=quantity)
        self.db.add(order_item)
        
        return order_item


