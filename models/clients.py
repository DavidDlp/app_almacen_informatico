from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base, Relation, db_session


class Client(Base):
    __tablename__ = 'clients'
    __table_args__ = {'sqlite_autoincrement': True}
    id_client = Column(Integer, primary_key=True)
    name = Column(String(20))
    lastname = Column(String(50))
    address = Column(String(150))
    country = Column(String(20))
    city = Column(String(25))
    cp = Column(Integer())
    phone = Column(String(20))
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, name, lastname, address, country, city, cp, phone, user_id):
        self.name = name
        self.lastname = lastname
        self.address = address
        self.country = country
        self.city = city
        self.cp = cp
        self.phone = phone
        self.user_id = user_id