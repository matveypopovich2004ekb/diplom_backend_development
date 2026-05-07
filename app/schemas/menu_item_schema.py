from pydantic import BaseModel, ConfigDict

class MenuItemInfo(BaseModel):
    """Схема данных блюда в Меню Заведения"""

    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str 


class Ingredient(BaseModel):
    """схема интгредиента блюда MenuItem для схемы MenuItemCreate"""

    product_id: int
    amount: float


class MenuItemCreate(BaseModel):
    """схема для создания пункта меню(нового блюда)"""

    name: str
    ingredients: list[Ingredient]



    
