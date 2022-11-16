from sqlalchemy import Column, Integer, ForeignKey
from db import Base, Relation

class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {'sqlite_autoincrement': True}
    order_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id_product"))
    user_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return f"Order: {self.order.id} --> {self.user_id} --> {self.product_id}"

    def __str__(self):
        return f"Order: {self.order.id} --> {self.user_id} --> {self.product_id}"
