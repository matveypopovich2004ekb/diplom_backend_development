from fastapi import APIRouter, status

from app.schemas.product_schema import ProductInfo

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
def get_product_list():
    response_list = [ProductInfo(**i) for i  in TestProductList]
    return response_list

