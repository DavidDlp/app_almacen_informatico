from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base, session


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}
    id_user = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(50), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id_role"))

    def __init__(self, username, name, role_id=2):
        self.username = username
        self.name = name = name
        self.role_id = role_id

    def __repr__(self):
        return f"User: {self.username} --> {self.name}"

    def __str__(self):
        return f"User: {self.username} --> {self.name}"

    def addAdmin():
        user_admin = User("Administrador", "Federico", role_id=1)
        session.add(user_admin)
        session.commit()
        session.close()

    def addInitialUser():
        user_test = User("Testeando", "Dexter")
        session.add(user_test)
        session.commit()
        session.close()