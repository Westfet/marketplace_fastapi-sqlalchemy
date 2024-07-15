from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.product_controller import ProductCreate, create_product, get_product
from queries.database import get_db

router = APIRouter()


@router.post("/", response_model=ProductCreate)
def create_product_view(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(product, db)


@router.get("/{product_id}", response_model=ProductCreate)
def get_product_view(product_id: int, db: Session = Depends(get_db)):
    return get_product(product_id, db)
