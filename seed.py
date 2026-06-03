from app.data_base.db_session import session_local_class
from app.models.all_models import (
    ProductORM,
    MenuORM,
    MenuItemIngredientORM,
    OrdersORM,
    OrderItemORM
    
)
from app.models.suppplier_models import SuppliersORM, SupplierOfferORM


def reset_database():
    db = session_local_class()

    try:
        # Удаляем сначала зависимые таблицы, потом основные
        db.query(SupplierOfferORM).delete()
        db.query(OrderItemORM).delete()
        db.query(OrdersORM).delete()
        db.query(MenuItemIngredientORM).delete()
        db.query(MenuORM).delete()
        db.query(ProductORM).delete()
        db.query(SuppliersORM).delete()

        db.commit()

        # -------------------------
        # 1. Продукты
        # -------------------------

        milk = ProductORM(
            name="Молоко",
            unit="ml",
            quantity=5000,
            critical_quantity=1000,
        )

        coffee = ProductORM(
            name="Зерна кофе",
            unit="g",
            quantity=3000,
            critical_quantity=650,
        )

        sugar = ProductORM(
            name="Сахар",
            unit="g",
            quantity=2000,
            critical_quantity=500,
        )

        db.add_all([milk, coffee, sugar])
        db.flush()

        # -------------------------
        # 2. Меню
        # -------------------------

        latte = MenuORM(name="Латте")
        cappuccino = MenuORM(name="Капучино")
        americano = MenuORM(name="Американо")

        db.add_all([latte, cappuccino, americano])
        db.flush()

        # -------------------------
        # 3. Состав блюд
        # -------------------------

        ingredients = [
            # Латте
            MenuItemIngredientORM(
                menu_item_id=latte.id,
                product_id=milk.id,
                amount=200,
            ),
            MenuItemIngredientORM(
                menu_item_id=latte.id,
                product_id=coffee.id,
                amount=30,
            ),
            MenuItemIngredientORM(
                menu_item_id=latte.id,
                product_id=sugar.id,
                amount=10,
            ),

            # Капучино
            MenuItemIngredientORM(
                menu_item_id=cappuccino.id,
                product_id=milk.id,
                amount=150,
            ),
            MenuItemIngredientORM(
                menu_item_id=cappuccino.id,
                product_id=coffee.id,
                amount=30,
            ),
            MenuItemIngredientORM(
                menu_item_id=cappuccino.id,
                product_id=sugar.id,
                amount=5,
            ),

            # Американо
            MenuItemIngredientORM(
                menu_item_id=americano.id,
                product_id=coffee.id,
                amount=30,
            ),
        ]

        db.add_all(ingredients)

        # -------------------------
        # 4. Поставщики
        # -------------------------

        suppliers = [
            SuppliersORM(name="barista_ltd"),
            SuppliersORM(name="napolke"),
            SuppliersORM(name="cofe_optom"),
        ]

        db.add_all(suppliers)

        # supplier_offers НЕ заполняем вручную.
        # Их позже будет создавать/обновлять парсер.

        db.commit()

        print("БД успешно перезаполнена тестовыми данными.")

    except Exception as exc:
        db.rollback()
        print("Ошибка при заполнении БД:", exc)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    reset_database()