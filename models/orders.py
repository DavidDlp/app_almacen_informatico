from sqlalchemy import Column, Integer, ForeignKey, Date
from db import Base

class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {'sqlite_autoincrement': True}
    order_id = Column(Integer, primary_key=True)
    creation_date = Column(Date)
    product_id = Column(Integer, ForeignKey("products.id_product"))
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, creation_date, product_id, user_id):
        self.creation_date = creation_date
        self.product_id = product_id
        self.user_id = user_id

    def __repr__(self):
        return f"Order: {self.order_id} --> {self.user_id} --> {self.product_id}"

    def __str__(self):
        return f"Order: {self.order_id} --> {self.user_id} --> {self.product_id}"
