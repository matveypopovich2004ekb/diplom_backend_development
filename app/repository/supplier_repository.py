from app.models.suppplier_models import  SupplierOfferORM, SuppliersORM


from typing import Sequence
from sqlalchemy import select

class SupplierRepository():

    def __init__(self, db):
        self.db = db

    def get_supplier_by_id(self, supplier_id: int) -> SuppliersORM | None:

        supplier = self.db.get(SuppliersORM, supplier_id)
        return supplier

    def get_supplier_offers_list_by_product_id(self, product_id: int) -> Sequence[SupplierOfferORM]:
        """"""

        supplier_offers = self.db.scalars(
            select(SupplierOfferORM).where(SupplierOfferORM.product_id == product_id)
        ).all()
        
        return supplier_offers

    def get_supplier_by_name(self, name: str) -> SuppliersORM | None:
        """ парсер присылает инфу с указанием назваания потсавщика, а не id
        поэтому нам нужен такой метод"""

        #получаем поставщика по его названию name
        supplier_by_name = self.db.scalar(
            select(SuppliersORM).where(SuppliersORM.name == name)
        ) 

        return supplier_by_name
    

    def get_offer_by_product_and_supplier_id(self, product_id: int, supplier_id) -> SupplierOfferORM | None:
        """ метод ищет и возвращает оффер из SupplierOfferORM с соответствующими product_id, supplier_id
        если если такого нет, то по идее возвращает None"""

        supplier_offer = self.db.scalar(
            select(SupplierOfferORM).where(
                SupplierOfferORM.supplier_id==supplier_id,
                SupplierOfferORM.product_id==product_id)
        )

        return supplier_offer #объект SupplierOfferORM

    def create_supplier_offer(self, supplier_id, product_id, price, package_quantity):

        new_offer = SupplierOfferORM(
            supplier_id=supplier_id, product_id=product_id,
            price=price, package_quantity=package_quantity
        ) 

        self.db.add(new_offer)

        
        
