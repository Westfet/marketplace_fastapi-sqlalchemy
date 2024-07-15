from sqlalchemy.orm import Session
from models.product import Product
from pydantic import BaseModel
from queries.database import session_factory
from fastapi import HTTPException


class ProductCreate(BaseModel):
    product_name: str
    price: float
    amount: int
    category_id: int
    shop_id: int


def create_product(product: ProductCreate, db: Session):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(product_id: int, db: Session):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
