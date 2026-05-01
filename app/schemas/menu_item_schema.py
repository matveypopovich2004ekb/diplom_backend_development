from pydantic import BaseModel, ConfigDict

class MenuItemInfo(BaseModel):
    """Схема данных блюда в Меню Заведения"""

    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str 

    