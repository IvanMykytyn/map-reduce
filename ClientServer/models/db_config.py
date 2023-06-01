from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import declarative_base

from ClientServer.constants import DATABASE_URI

engine = create_engine(DATABASE_URI)

# create a scoped session factory
Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

# associate the session with the Base class
Base.query = Session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
