from fastapi import APIRouter, status, Depends

from app.schemas.supplier_schema import SupplierOfferInfo, SupplierParseResponse
from app.schemas.order_schema import SimulateOrderRequest, SimulateOrderResponse
from app.schemas.product_schema import ProductInfo, ProductCreate, ProductUpdate
from app.schemas.menu_item_schema import MenuItemInfo, MenuItemCreate
from app.routers.dependencies import get_product_service, get_menu_service, get_simulate_order_service, get_supplier_service

router = APIRouter(prefix="/api")



# получаем список продуктов
@router.get(
    "/products", # маршрут правильно указал?
    response_model=list[ProductInfo], status_code=status.HTTP_200_OK
            )
def get_product_list(service = Depends(get_product_service)) -> list[ProductInfo]:
    response_list = service.get_product_list()
    return response_list


#получаем список блюда в меню
@router.get("/menu-items", 
            status_code=status.HTTP_200_OK, response_model=list[MenuItemInfo]
            ) 
def get_menu_list(service = Depends(get_menu_service)) -> list[MenuItemInfo]:
    response_list = service.get_menu_list()
    return response_list
    
#проводим покупку
@router.post("/orders/simulate", 
             status_code=status.HTTP_201_CREATED, response_model=SimulateOrderResponse
             )
def new_order(payload: SimulateOrderRequest, 
              service=Depends(get_simulate_order_service)) -> SimulateOrderResponse:
    
    response = service.order_processing(payload=payload)

    return response

#создаем новый продукт
@router.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductInfo)
def create_product(payload: ProductCreate, 
                   service = Depends(get_product_service)) -> ProductInfo:
    
    response = service.create_new_product(payload=payload)
    return response

@router.patch("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductInfo)
def update_product(product_id: int,
                    payload: ProductUpdate, 
                   service = Depends(get_product_service)) -> ProductInfo:
    
    response = service.update_product(product_id=product_id, payload=payload)
    return response
    
@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def create_product(product_id: int,
                   service = Depends(get_product_service)) -> None:
    
    result = service.delete_product(product_id=product_id)
    return 


# добавить блюдо в Меню
@router.post("/menu-items", status_code=status.HTTP_201_CREATED, response_model=MenuItemInfo)
def create_menu_item(payload:  MenuItemCreate, service = Depends(get_menu_service)):

    response = service.create_new_menu_item(payload)
    return response
    

# обновление предложений поставщиков
@router.post("/supplier-offers/parse/coffee",
              status_code=status.HTTP_201_CREATED, 
              response_model=SupplierParseResponse)
def response_aboute_update_of_offers(service = Depends(get_supplier_service)):
    
    response = service.update_suppliers_offers()
    return response


@router.get("/products/{product_id}/supplier-offers", 
            response_model = list[SupplierOfferInfo],
            status_code=status.HTTP_200_OK)
def get_suppliers_list(product_id: int, service = Depends(get_supplier_service)):

    response = service.get_suppliers_offers_list(product_id)
    return response



