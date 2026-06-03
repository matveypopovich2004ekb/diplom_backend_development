from pydantic import BaseModel


class SupplierOfferInfo(BaseModel):
    supplier_name: str
    price: float
    package_quantity: float
    unit: str
    price_per_unit: float


class SupplierParseResponse(BaseModel):
    message: str
    updated_count: int



