import json
from queries.orm import SyncORM
from sqlalchemy.orm import Session
from queries.database import session_factory
from models import User, Shop, Category, Product

# Путь к JSON-файлу
DATA_FILE = "db_data.json"


def load_data_from_json(db: Session, file_path: str):
    with open(file_path, "r") as file:
        data = json.load(file)

    for user_data in data['users']:
        user = User(**user_data)
        db.add(user)

    for shop_data in data['shops']:
        shop = Shop(**shop_data)
        db.add(shop)

    for category_data in data['categories']:
        category = Category(**category_data)
        db.add(category)

    for product_data in data['products']:
        product = Product(**product_data)
        db.add(product)

    db.commit()


def main():
    SyncORM.create_tables()
    db = session_factory()
    try:
        load_data_from_json(db, DATA_FILE)
        print("Data successfully loaded from JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
