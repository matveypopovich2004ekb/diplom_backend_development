# здесь лежат функции, которые возращают объект сервиса

from fastapi import Depends
from sqlalchemy.orm import Session

from app.service.order_simulate_service import ProductService, MenuService, SimulateOrderService
from app.data_base.db_session import get_database

def get_product_service(db: Session = Depends(get_database)):
    return ProductService(db)

def get_menu_service(db: Session = Depends(get_database)):
    return MenuService(db)

def get_simulate_order_service(db: Session = Depends(get_database)):
    return SimulateOrderService(db)