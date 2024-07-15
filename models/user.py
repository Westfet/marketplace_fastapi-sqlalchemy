from queries.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    phone_number: Mapped[str] = mapped_column(String(12), unique=True)

    # связь с Order
    user_orders: Mapped[list["Order"]] = relationship("Order", back_populates='order_from_user')

    # связь с Review
    user_reviews: Mapped[list["Review"]] = relationship("Review", back_populates='review_writer')
