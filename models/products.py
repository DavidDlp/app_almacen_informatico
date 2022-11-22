from sqlalchemy import Column, Integer, String, Numeric, Boolean
from db import Base, db_session, Relation
from models.orders import Order
from models.applyFor import Apply

class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'sqlite_autoincrement': True}
    id_product = Column(Integer, primary_key=True)
    product_name = Column(String(50), nullable=False)
    mark = Column(String(50))
    type = Column(String(30))
    sale_price = Column(Numeric(10, 2))
    purchase_price = Column(Numeric(10, 2))
    quantity = Column(Integer(), nullable=False)
    description = Column(String(255), nullable=False)
    image = Column(String(30))
    order = Relation("Order", backref="product")
    apply = Relation("Apply", backref="product")


    def __init__(self, product_name, mark, type, sale_price, purchase_price, quantity, description, image="../static/image/image-db/image-default.jpg"):
        self.product_name = product_name
        self.mark = mark
        self.type = type
        self.sale_price = sale_price
        self.purchase_price = purchase_price
        self.quantity = quantity
        self.description = description
        self.image = image


    def __repr__(self):
        return f"Product: {self.id_product} --> {self.product_name}, {self.description}"

    def __str__(self):
        return f"Product: {self.id_product} --> {self.product_name}, {self.description}"

def addInitialProducts():
    p1 = Product("teclado Nisu", "nisu", "Perifericos", 20.5, 17, 10, "Teclado común de marca desconocida", "../static/image/image-db/keyboard.png" )
    p2 = Product("raton Nisu", "nisu", "Perifericos", 12, 9.5, 10, "Raton común de marca desconocida")
    p3 = Product("portatil Msi", "MSI", "Portatiles", 1200.25, 950.50, 10, "Portatil i7 16GB de RAM 15.6 pulgadas",  "../static/image/image-db/laptop.jpg")
    p4 = Product("camara web Nisu", "Trush", "Perifericos", 30.5, 25, 10, "camara HD 1080P con microfono incorporado")
    p5 = Product("iPhone 13", "Apple", "Smartphones", 990, 770, 10, "movil de ultima geeneración", "../static/image/image-db/smartphone-iphone.png")
    p6 = Product("teclado & raton inalambricos Trush", "Perifericos", "Trush", 45.25, 32.50, 10, "Teclado y raton común inalambricos ", "../static/image/image-db/mouse-keyboard.png")
    db_session.add_all([p1, p2, p3, p4, p5, p6])
    db_session.commit()
    db_session.close()
