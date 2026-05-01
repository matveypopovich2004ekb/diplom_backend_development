from pydantic import BaseModel, ConfigDict


from app.schemas.product_schema import UsedProduct


class SimulateOrderItem(BaseModel):
    """информация об одном из блюд заказа и его количестве(например 2 Латте)"""

    menu_item_id: int
    quantity: int

class SimulateOrderRequest(BaseModel):
    """схеама заказа, который прихожит с фонтенда"""

    items: list[SimulateOrderItem]


class SimulateOrderResponse(BaseModel):
    """схема ответа по заказу на фронтенд"""

    model_config = ConfigDict(from_attributes=True)

    order_id: int
    used_products: list[UsedProduct]
