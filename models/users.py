from flask_login import UserMixin
# database
from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base, Relation, db_session
from models.orders import Order


class User(Base, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True, index=True)
    password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id_role"))
    order = Relation("Order", backref="user")

    def __init__(self, username, password, role_id=2):
        self.username = username
        self.password = password
        self.role_id = role_id

    def __repr__(self):
        return f"User: {self.username} --> {self.role_id}"

    def __str__(self):
        return f"User: {self.username} --> {self.role_id}"

def addAdmin():
    user_admin = User("Administrador",
                      "$2b$12$tQPomBKPzxblsY0Pncox6uiBZ8kN92usHRtM/bitHvO0zpEKgeVL6",
                       role_id=1)
    db_session.add(user_admin)
    db_session.commit()
    db_session.close()


def addInitialUser():
    user_test = User("Cliente",
                     "$2b$12$6Soo91Akh3WY/bcbj8iG/O0nxviDVnFmHoo5rXewd7drKZoihm.Re")
    db_session.add(user_test)
    db_session.commit()
    db_session.close()

def addInitialSupplier():
    supplier_test = User("Proveedor", "$2b$12$1M277OQJRJOCQuRPKwjUOuWd8vbsmXUOOL2txEPshTh1cYxaY77A6", 3)
    db_session.add(supplier_test)
    db_session.commit()
    db_session.close()
