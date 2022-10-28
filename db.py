from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Engine
engine = create_engine('sqlite:///database/almacen_informatico.db', connect_args={'check_same_thread': False})

# Session
Session = sessionmaker(bind=engine)
session = Session()

Relation = relationship
Base = declarative_base()