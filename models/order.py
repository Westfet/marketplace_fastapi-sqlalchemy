import enum

from sqlalchemy import ForeignKey
from config import CREATED_AT
from queries.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderStatus(enum.Enum):
    success = 'доставлен'
    in_process = 'в процессе'
    canceled = 'отменен'


class Order(Base):
    __tablename__ = 'orders'

    status: Mapped[OrderStatus]
    created_at: Mapped[CREATED_AT]

    # Связь m2m с Product
    order_size: Mapped[list["Product"]] = relationship("Product", back_populates='product_in_orders',
                                                       secondary='order_items')

    # Связь с User
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    order_from_user: Mapped["User"] = relationship("User", back_populates="user_orders")
