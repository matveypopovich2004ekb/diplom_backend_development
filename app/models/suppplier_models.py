from app.models.basic_model import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.schema import UniqueConstraint


class SuppliersORM(Base):
    """список пооставщиков"""

    __tablename__ = "suppliers"

    name: Mapped[str]


class SupplierOfferORM(Base):
    """предложения пооставщиков"""

    __tablename__ = "supplier_offers"

    __table_args__ = (# чтобы не было дублликатов
        UniqueConstraint(
            "supplier_id",
            "product_id",
            name="uq_supplier_product_offer",
        ),
    )

    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    price: Mapped[float | None]
    package_quantity: Mapped[float | None]
    # единицы измеерения возьмем потом из ProductORM

    @property
    def price_per_unit(self):
        # прежде чем рассчитывать этот параметр, надо убедиться в том, 
        # что мы имеем числовые значения параметров после работы парсера, 
        # а не None или 0
        if self.price is None or self.package_quantity is None or self.package_quantity == 0:
            return None
        
        return round(self.price/self.package_quantity, 4)
    

