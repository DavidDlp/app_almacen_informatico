from flask_login import UserMixin
# database
from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base, db_session


class Supplier(Base, UserMixin):
    __tablename__ = 'suppliers'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True, index=True)
    password = Column(String(100), nullable=False)
    business = Column(String(50))
    role_id = Column(Integer, ForeignKey("roles.id_role"))

    def __init__(self, username, password, business=None, role_id=3):
        self.username = username
        self.password = password
        self.business = business
        self.role_id = role_id

    def __repr__(self):
        return f"Proveedor: {self.username} --> {self.business}"

    def __str__(self):
        return f"Proveedor: {self.username} --> {self.business}"

def addInitialSup():
    sup_test = Supplier("Testeando",
                     "$2b$12$1M277OQJRJOCQuRPKwjUOuWd8vbsmXUOOL2txEPshTh1cYxaY77A6",
                     "Nisu")
    db_session.add(sup_test)
    db_session.commit()
    db_session.close()
