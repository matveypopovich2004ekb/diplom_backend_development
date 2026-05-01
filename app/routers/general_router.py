from fastapi import APIRouter, status, Depends

from app.schemas.order_schema import SimulateOrderRequest, SimulateOrderResponse
from app.schemas.product_schema import ProductInfo
from app.schemas.menu_item_schema import MenuItemInfo
from app.routers.dependencies import get_product_service, get_menu_service, get_simulate_order_service

router = APIRouter(prefix="/api")


TestProductList = [
    {"id": 1,
    "name": "Молоко",
    "unit": "ml",
    "quantity": 5000,
    "critical_quantity": 1000},

    {"id": 2,
    "name": "Зерна кофе",
    "unit": "g",
    "quantity": 3000,
    "critical_quantity": 6500}
]


@router.get(
    "/products", # маршрут правильно указал?
    response_model=list[ProductInfo], status_code=status.HTTP_200_OK
            )
def get_product_list(service = Depends(get_product_service)) -> list[ProductInfo]:
    response_list = service.get_product_list()
    return response_list



@router.get("/menu-items", 
            status_code=status.HTTP_200_OK, response_model=list[MenuItemInfo]
            ) 
def get_menu_list(service = Depends(get_menu_service)) -> list[MenuItemInfo]:
    response_list = service.get_menu_list()
    return response_list
    

@router.post("/orders/simulate", 
             status_code=status.HTTP_201_CREATED, response_model=SimulateOrderResponse
             )
def new_order(payload: SimulateOrderRequest, 
              service=Depends(get_simulate_order_service)) -> SimulateOrderResponse:
    
    response = service.order_processing(payload=payload)

    return response
    




