from app.repository.order_simulate_repository import ProductRepository, MenuRepository, SimulateOrderRepository

from app.schemas.product_schema import ProductInfo, UsedProduct
from app.schemas.menu_item_schema import MenuItemInfo
from app.schemas.order_schema import SimulateOrderRequest, SimulateOrderResponse


from sqlalchemy.orm import Session
from fastapi import Depends

class ProductNotFound(Exception):
    pass


class ProductService():
    """ """

    def __init__(self,  db: Session):
        self.db = db
        self.repository = ProductRepository(db=db)

    def get_product_list(self):
        product_list = self.repository.get_list()
        return [ProductInfo.model_validate(i) for i in product_list]
    
    def edit_product_quantity_by_product_id(self, product_id: int, used_quantity: float) -> tuple[float, str, str]: 
        """метод будет вычитать количество товара по id.
           если в БД недостаточный запас какого-то продукта - не сохранит изменения и вернет False
        ВАЖНО!!! ПОКА ЧТО МЕХАНИКА С ПРОВЕРКОЙ ОПЕРАЦИИ НЕ РЕАЛИЗОВАНА"""
        
        product = self.repository.get_by_id(product_id=product_id) # получаем нужный продукт из БД
        if product is None: #это если продукт не найден в БД
            raise ProductNotFound(f"Product with id={product_id} not found")
        
        if product.quantity < used_quantity:
            raise ValueError(f"Недостаточно продукта id={product_id}")
        product.quantity -= used_quantity # уменьшаем у продукта его количество
        # ТУТ НАДО  ДОБАВИТЬ ПРОВЕРКУ НА ТО, ХВАТАЕТ ЛИ ПРОДУКТА НА ЗАКАЗ ВООБЩЕ,
        # ЧТОБЫ НЕ ПОЛУЧИТЬ ОТРИЦАТЕЛЬНОЕ КОЛИЧЕСТВО
        
        # возвращаем остаток продукта для remaining_quantity, название продукта и его ед. измерения
        return product.quantity, product.name, product.unit # возвращаем остаток продукта для remaining_quantity

class MenuService():
    """ """

    def __init__(self,  db: Session):
        self.db = db
        self.repository = MenuRepository(db=db)

    def get_menu_list(self):
        menu_list = self.repository.get_list()
        return [MenuItemInfo.model_validate(i) for i in menu_list]
    

class SimulateOrderService():
        def __init__(self,  db: Session):
            self.db = db
            self.repository = SimulateOrderRepository(db=db)    
            self.product_service = ProductService(db)

        
        def order_processing(self, payload: SimulateOrderRequest) -> SimulateOrderResponse:
            """ """

            try:
                used_products = [] # это потом будем использовать для SimulateOrderResponse

                order_item_list = payload.items # список из SimulateOrderItem()
                # поля для used_product_list: menu_item_id, quantity
                products_used_quantity = {} # {product_id : used_quantity}

                for order_item in order_item_list: # order_item ЭТО SimulateOrderItem()

                    ingredients = self.repository.MenuItemIngredientORM_from_menu_item_id(
                        order_item.menu_item_id
                    )
                    if not ingredients:
                        raise ValueError(f"Для блюда id={order_item.menu_item_id} не найден состав")

                    quantity = order_item.quantity # количество блюд с заказе (типо 2 Латте допусти)

                    for ingredient in ingredients: # ingredient это MenuItemIngredientORM()

                        amount = ingredient.amount  # количество продукта в блюде (типо 50 мг)
                        used_quantity = amount * quantity # итог - сколько продукта ушло на блюдо (к примеру 50 * 2 = 100)
                        products_used_quantity[ingredient.product_id] = (
                            products_used_quantity.get(ingredient.product_id, 0) + used_quantity
                        ) 

                #на этом моменте мы уже получили список словарей {product_id : used_quantity}
                # теперь нам надо вычесть необходимое количество кажд. товара в ProductORM

                for product_id, used_quantity in products_used_quantity.items():

                    remaining_quantity, product_name, product_unit = self.product_service.edit_product_quantity_by_product_id(
                            product_id=product_id,
                            used_quantity=used_quantity
                        ) 
                    
                    used_products.append(UsedProduct(
                        product_id=product_id,
                        name=product_name,
                        used_quantity=used_quantity,
                        unit=product_unit,
                        remaining_quantity=remaining_quantity
                        ))
                    
                self.db.commit()

                return SimulateOrderResponse(order_id=1, used_products=used_products)

            except Exception:
                self.db.rollback()
                raise
                


    













