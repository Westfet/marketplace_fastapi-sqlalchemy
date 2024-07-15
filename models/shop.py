from queries.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


# Не стал добавлять отдельно столбец продавцы (shop - универсальное поле для всех юр.лиц)
class Shop(Base):
    __tablename__ = 'shops'

    shop_name: Mapped[str] = mapped_column(String(256), nullable=False)
    address: Mapped[str] = mapped_column(String(256), unique=True)
    products: Mapped[list["Product"]] = relationship("Product", back_populates='shop')
