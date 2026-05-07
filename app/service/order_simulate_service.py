from app.repository.order_simulate_repository import ProductRepository, MenuRepository, SimulateOrderRepository

from app.schemas.product_schema import ProductInfo, UsedProduct, ProductCreate
from app.schemas.menu_item_schema import MenuItemInfo, MenuItemCreate
from app.schemas.order_schema import SimulateOrderRequest, SimulateOrderResponse

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

class ProductNotFound(Exception):
    pass


class ProductService():
    """ """

    def __init__(self,  db: Session):
        self.db = db
        self.repository = ProductRepository(db=db)

    def get_product_list(self) -> list[ProductInfo]:
        product_list = self.repository.get_list()
        
        return [ProductInfo.model_validate(i) for i in product_list]
    
    def create_new_product(self, payload: ProductCreate):

        product_atributes = payload.model_dump()

        #мы должны  проверить каждое поле продукта на то, что оно не пустое
        for atribute in product_atributes.values():
             if not str(atribute).strip(): #True если поле пустое / состоит только из пробелов
                 raise ValueError("заполняемое поле не может быть пустым при создании нового объекта")
        
        new_product = self.repository.create(product_atributes=product_atributes)
        self.db.commit()

        return ProductInfo.model_validate(new_product)

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

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

class MenuService():
    """ """

    def __init__(self,  db: Session):
        self.db = db
        self.repository = MenuRepository(db=db)

    def get_menu_list(self) -> list[MenuItemInfo]:
        menu_list = self.repository.get_list()
        return [MenuItemInfo.model_validate(i) for i in menu_list]
    
    def create_new_menu_item(self, payload: MenuItemCreate) -> MenuItemInfo:
        """созадает новое блюдо(элемент меню)"""

        # сначала надо добавить само блюдо в MenuORM
        name = payload.name
        if not name.strip(): # проверка что поле name не пустое
            raise ValueError(f"поле для заполнения name не может быть пустым")
        
        new_menu_item = self.repository.create_menu_item(name=name)

        # теперь мы должны заполнить для данного Menu Item ингредиенты MenuItemIngredientORM
        product_id_full_list = ProductRepository(db=self.db).get_ids_list() # получаем список всех id продуктов
        
        ingredients = payload.ingredients #список из Ingredient со полями product_id и amount
        for ingr in ingredients: #перебор всех ингредиентов нового блюда
            menu_item_id, product_id, amount = new_menu_item.id, ingr.product_id, ingr.amount

            # проведим необходимую валюдацию данных
            if not str(product_id).strip() or not str(amount).strip() or amount <= 0: # проверям значения полей
                raise ValueError("поля ингредиента не могут быть пустыми или <= 0")
            if product_id not in product_id_full_list:  # проверям, что указанный ингредиент имеется в списке продуктв
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="id ингредиента не найден в списке id продуктов")
            
            # добавляем каждый ингредиент и сколько его соделжится в нашем new_menu_item
            new_ingr = self.repository.create_ingredient_for_menu_item( 
                menu_item_id = menu_item_id, 
                product_id = product_id, 
                amount = amount
            )

        self.db.commit()
        return MenuItemInfo.model_validate(new_menu_item) 

        
    

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

class SimulateOrderService():
        def __init__(self,  db: Session):
            self.db = db
            self.repository = SimulateOrderRepository(db=db)    
            self.product_service = ProductService(db)

        
        def order_processing(self, payload: SimulateOrderRequest) -> SimulateOrderResponse:
            """ """

            try:
                order = self.repository.create_new_order() # добавляем в таблицу заказов заказ
                self.db.flush()

                used_products = [] # это потом будем использовать для SimulateOrderResponse

                order_item_list = payload.items # список из SimulateOrderItem()
                # поля для used_product_list: menu_item_id, quantity
                products_used_quantity = {} # {product_id : used_quantity}

                for order_item in order_item_list: # order_item ЭТО SimulateOrderItem()
                    
                    self.repository.create_new_order_item(
                        order_id=order.id, 
                        menu_item_id= order_item.menu_item_id,
                        quantity=order_item.quantity
                    ) # добавляем в таблицу OrderItemORM строку

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
                    # готовим ответ на фронтенд, собирая объекты UsedProduct() в список
                    used_products.append(UsedProduct(
                        product_id=product_id,
                        name=product_name,
                        used_quantity=used_quantity,
                        unit=product_unit,
                        remaining_quantity=remaining_quantity
                        ))
                
                
                


                self.db.commit()

                return SimulateOrderResponse(order_id=order.id, used_products=used_products)

            except Exception:
                self.db.rollback()
                raise
                


    













