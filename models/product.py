from queries.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class Product(Base):
    __tablename__ = 'products'

    # TODO разобраться, как исключить добавление отрицательных значений в price и amount
    product_name: Mapped[str] = mapped_column(String(256), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    # связи с Category
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    category: Mapped["Category"] = relationship('Category', back_populates="products")
    # связи с Shop
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id", ondelete='CASCADE'))
    shop: Mapped["Shop"] = relationship("Shop", back_populates="products")
    # связи c Order
    product_in_orders: Mapped[list["Order"]] = relationship("Order", back_populates="order_size",
                                                            secondary='order_items')
    # связи с Review
    product_reviews: Mapped[list["Review"]] = relationship("Review", back_populates='scored_product')
