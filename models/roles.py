from sqlalchemy import Column, Integer, String
from db import Base, db_session, Relation


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'sqlite_autoincrement': True}
    id_role = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    users = Relation("User", backref="role")

    def __repr__(self):
        return "<Role %r>" %self.name

    def __str__(self):
        return "<Role %r>" %self.name

# Creamos los roles que se asignaran alos usuarios y/o proveedores
def addRole():
        admin_role = Role(name="Admin")
        user_role = Role(name="User")
        supplier_role = Role(name="Supplier")
        db_session.add_all([admin_role, user_role, supplier_role])
        db_session.commit()
        db_session.close()
