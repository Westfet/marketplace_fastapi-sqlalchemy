from queries.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class Review(Base):
    __tablename__ = 'reviews'

    review: Mapped[str] = mapped_column(String(500))
    rating: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    review_writer: Mapped["User"] = relationship("User", back_populates='user_reviews')

    scored_product: Mapped["Product"] = relationship("Product", back_populates='product_reviews')