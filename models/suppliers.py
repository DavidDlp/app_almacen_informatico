from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base, Relation, db_session


class Supplier(Base):
    __tablename__ = 'supplier'
    __table_args__ = {'sqlite_autoincrement': True}
    id_supplier = Column(Integer, primary_key=True)
    company_name = Column(String(50))
    country = Column(String(20))
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, company_name, country, user_id):
        self.company_name = company_name
        self.country = country
        self.user_id = user_id

def addProfileInitialSupplier():
    profile_supplier_test = Supplier("Nisu", "España", 3)
    db_session.add(profile_supplier_test)
    db_session.commit()
    db_session.close()

