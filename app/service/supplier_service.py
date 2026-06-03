from app.parsers.run_parsers import parse_all_coffee_offers
from app.repository.order_simulate_repository import ProductRepository
from app.repository.supplier_repository import SupplierRepository
from app.schemas.supplier_schema import SupplierParseResponse, SupplierOfferInfo


from fastapi import HTTPException, status


"""
это я добавил просто чтобы видеть поля, которые возвращает парсер

{
    "supplier": "barista_ltd",
    "product_name": "Кофе в зернах AltaRoma Arabica 1000 г",
    "price": 1451.48,
    "price_raw": "от 1 451.48 руб.",
    "package_quantity": "1000 г",
    "package_quantity_raw": "1000 г",
    "url": "https://www.barista-ltd.ru/magazin/kofe-v-zernakh-almafood-altaroma-arabica-1kg.html"
  },""" 


class SupplierService():
    """сервис, отвечающий за работу с поставщиками"""
    def __init__(self, db):
        self.db = db
        self.repository = SupplierRepository(db=db)





    def get_suppliers_offers_list(self, product_id) -> list[SupplierOfferInfo]:
        """Выводим список предложений всех поставщиков по выбранному продукту(по его id)"""

        response_list = [] #list[SupplierOfferInfo] - готовим на ответ фронту
        product_repository = ProductRepository(db=self.db)

        #проверка, что продукт с таким Id вообще есть в списке продуктов
        product = product_repository.get_by_id(product_id=product_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Продукта с id {product_id} нет в ProductORM!")

        product_unit = product.unit

        # получили список офферов типа SupplierOfferORM с нужным product_id
        supplier_offers = self.repository.get_supplier_offers_list_by_product_id(product_id=product_id)


        #тeпкрь достаем название  поставщика по его id
        for offer in supplier_offers:
            supplier = self.repository.get_supplier_by_id(supplier_id=offer.supplier_id)

            if supplier is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Поставщика с id {offer.supplier_id} нет в SuppliersORM!")
            
            supplier_name = supplier.name

            offer_info = SupplierOfferInfo(
                supplier_name=supplier_name, price=offer.price, package_quantity=offer.package_quantity,
                unit=product_unit, price_per_unit=offer.price_per_unit
            )

            response_list.append(offer_info)
        return response_list


    def update_suppliers_offers(self) -> SupplierParseResponse:
        """Выполняем парсинг поставщиков и обновляем предложения в БД"""

        try:
            pars_offers = parse_all_coffee_offers() #получаем список предложений по всем трем поставщикам list[ProductOffer]
            
            if not pars_offers:
                raise HTTPException(
                    detail="Парсер не вернул ни одного предложения",
                )
            #далее нам будут нужны эти 2 репозитория
            product_repository = ProductRepository(db=self.db)

            for offer in pars_offers: 
                #берем все нужные параметры по предложению с с парсера
                supplier_name = offer.supplier
                product_name = offer.product_name
                price = offer.price
                package_quantity = offer.package_quantity


                #получаем id продукта из его названия
                
                product_by_name = product_repository.get_product_by_name(product_name) # ProductORM()
                if product_by_name is None: # если вдруг продукт с таким назваанием не найден в БД ProductORM
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"Продукт с названием {product_name} не найден")
                product_id = product_by_name.id
                
                #таким же образом получаем id поставщика из его названия
                
                suppllier_by_name= self.repository.get_supplier_by_name(supplier_name) # SuppliersORM()
                if suppllier_by_name is None: # если вдруг поставщик с таким назваанием не найден в БД SuppliersORM
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"Поставщик с названием {supplier_name} не найден")
                supplier_id = suppllier_by_name.id


                #получаем соответствующий оффер из БД, если он там вообще есть,
                #  а если его там  нет - создаем
                current_offer = self.repository.get_offer_by_product_and_supplier_id(
                    product_id=product_id,
                    supplier_id=supplier_id
                )
                
                if current_offer is None:
                    #здесь надо создать новый оффер
                    self.repository.create_supplier_offer(
                        supplier_id=supplier_id, product_id=product_id,
                        price=price, package_quantity=package_quantity
                    )

                else:
                    # здесь мы просто обновляем данные по офферу, если такой уже существует(и мы его получили в current_offer)
                    current_offer.price = price
                    current_offer.package_quantity = package_quantity

            self.db.commit()
            return SupplierParseResponse(
                message= "Предложения по зерновому кофе обновлены",
                updated_count=len(pars_offers)
            )

        except Exception:
            self.db.rollback()
            raise 






