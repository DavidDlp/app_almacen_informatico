
from werkzeug.security import check_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base, session


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}
    id_user = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True,  index=True)
    password = Column(String(150), unique=True)
    name = Column(String(50))
    role_id = Column(Integer, ForeignKey("roles.id_role"))


    def __init__(self, username, password, name ="", role_id=2):
        self.username = username
        self.password = password
        self.name = name
        self.role_id = role_id

    def __repr__(self):
        return f"User: {self.username} --> {self.name}"

    def __str__(self):
        return f"User: {self.username} --> {self.name}"

    @classmethod
    def check_password(self, hash_password, password):
        return check_password_hash(hash_password, password)

def addAdmin():
        user_admin = User("Administrador", "pbkdf2:sha256:260000$cfzlwvOJL2VXhluv$21eafd6e64c50a40fb2330648eafce154502c57dacf1c86d0a58b936967921e2", "Federico", role_id=1)
        session.add(user_admin)
        session.commit()
        session.close()

def addInitialUser():
        user_test = User("Testeando", "pbkdf2:sha256:260000$Uuz7LjONYMg4c3Uw$78fe679ad8b437e73bbe05851899357df421d537e9e3c3890de9b652568c0316", "Dexter")
        session.add(user_test)
        session.commit()
        session.close()