from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, scoped_session

# Engine
engine = create_engine('sqlite:///database/almacen_informatico.db', connect_args={'check_same_thread': False})

# Session
db_session = scoped_session(sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=engine))

Relation = relationship
Base = declarative_base()
Base.query = db_session.query_property()