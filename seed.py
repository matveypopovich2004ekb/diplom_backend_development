from app.data_base.db_session import session_local_class
from app.models. all_models import ProductORM, MenuORM, MenuItemIngredientORM


def seed_database():
    db_session = session_local_class()

    try:
        # Проверяем, не заполнена ли база уже
        existing_product = db_session.query(ProductORM).first()
        if existing_product:
            print("База уже содержит продукты. Seed отменён.")
            return

        # 1. Продукты
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

        db_session.add_all([milk, coffee, sugar])
        db_session.commit()

        db_session.refresh(milk)
        db_session.refresh(coffee)
        db_session.refresh(sugar)

        # 2. Блюда меню
        latte = MenuORM(name="Латте")
        cappuccino = MenuORM(name="Капучино")
        americano = MenuORM(name="Американо")

        db_session.add_all([latte, cappuccino, americano])
        db_session.commit()

        db_session.refresh(latte)
        db_session.refresh(cappuccino)
        db_session.refresh(americano)

        # 3. Состав блюд
        ingredients = [
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

            MenuItemIngredientORM(
                menu_item_id=americano.id,
                product_id=coffee.id,
                amount=30,
            ),
        ]

        db_session.add_all(ingredients)
        db_session.commit()

        print("Тестовые данные успешно добавлены.")

    except Exception as error:
        db_session.rollback()
        print("Ошибка при заполнении БД:", error)

    finally:
        db_session.close()


if __name__ == "__main__":
    seed_database()