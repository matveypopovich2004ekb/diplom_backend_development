from pydantic import BaseModel, ConfigDict

class ProductInfo(BaseModel):
    """Схема данных Продукта"""
    
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    unit: str #в чем измеряется количество товара
    quantity: float
    critical_quantity: float
    is_critical: bool # проверяет, хватает ли продукта на складе


class ProductCreate(BaseModel):
    """Схема данных для создания нового Продукта"""
    
    model_config = ConfigDict(from_attributes=True)

    name: str
    unit: str #в чем измеряется количество товара
    quantity: float
    critical_quantity: float



class UsedProduct(BaseModel):
    """схема данных о продукте после заказа - че за продукт, сколько убыло, какой остаток и т.д."""

    model_config = ConfigDict(from_attributes=True)

    product_id: int
    name: str
    used_quantity: float
    unit: str
    remaining_quantity: float