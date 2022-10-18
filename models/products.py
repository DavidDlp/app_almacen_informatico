from sqlalchemy import Column, Integer, String
from db import Base

class Product(Base):

    __tablename__ = 'product'
    __table_args__ = {'sqlite_autoincrement': True}
    id_product = Column(Integer, primary_key=True)
    product_name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)

    def __init__(self,product_name, description):
        self.product_name = product_name
        self.description = description

    def __repr__(self):
        return f"Product: {self.id_product} --> {self.product_name}, {self.description}"

    def __str__(self):
        return f"Product: {self.id_product} --> {self.product_name}, {self.description}"

