from .session import engine
from .base import Base


def init_db():
    print("***** create tables ")
    Base.metadata.create_all(bind=engine)
