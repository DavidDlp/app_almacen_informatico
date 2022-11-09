from sqlalchemy import Column, Integer, String, Numeric, Boolean
from db import Base, db_session, Relation
from models.orders import Order

class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'sqlite_autoincrement': True}
    id_product = Column(Integer, primary_key=True)
    product_name = Column(String(50), nullable=False)
    mark = Column(String(50))
    price = Column(Numeric(10, 2))
    quantity = Column(Integer(), nullable=False)
    description = Column(String(255), nullable=False)
    stock = Column(Boolean)
    image = Column(String(30))
    order = Relation("Order", backref="product")


    def __init__(self, product_name, mark, price, quantity, description, stock, image="../static/image/image-db/image-default.jpg"):
        self.product_name = product_name
        self.mark = mark
        self.price = price
        self.quantity = quantity
        self.description = description
        self.stock = stock
        self.image = image


    def __repr__(self):
        return f"Product: {self.id_product} --> {self.product_name}, {self.description}"

    def __str__(self):
        return f"Product: {self.id_product} --> {self.product_name}, {self.description}"

    def addInitialProducts():
        p1 = Product("teclado", "nisu", 20.5, 10, "Teclado común de marca desconocida", True, "../static/image/image-db/keyboard.png" )
        p2 = Product("raton", "nisu", 12, 10, "Raton común de marca desconocida", True)
        p3 = Product("portatil", "MSI", 1200.25, 10, "Portatil i7 16GB de RAM 15.6 pulgadas", True,  "../static/image/image-db/laptop.jpg")
        p4 = Product("camara web", "Trush", 30.5, 10, "camara HD 1080P con microfono incorporado", True)
        p5 = Product("iPhone 13", "Apple", 990, 10, "movil de ultima geeneración", True, "../static/image/image-db/smartphone-iphone.png")
        p6 = Product("teclado & raton inalambricos", "Trush", 45.25, 10, "Teclado y raton común inalambricos ", True, "../static/image/image-db/mouse-keyboard.png")
        db_session.add_all([p1, p2, p3, p4, p5, p6])
        db_session.commit()
        db_session.close()
