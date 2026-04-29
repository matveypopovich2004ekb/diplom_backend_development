from pydantic import BaseModel

class ProductInfo(BaseModel):
    id: int
    name: str
    unit: str #в чем измеряется количество товара
    quantity: float
    critical_quantity: float

