from queries.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


class Category(Base):
    __tablename__ = 'categories'

    # TODO возможно нужна связь m2m, у товара может быть несколько категорий
    category_name: Mapped[str] = mapped_column(String(256), nullable=False)
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")
