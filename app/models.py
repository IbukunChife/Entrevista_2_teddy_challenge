from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text, Boolean

Base = declarative_base()


class Teddy360(Base):
    __tablename__ = "teddy_360"

    id = Column(Integer, primary_key=True)
    userId = Column(Integer)
    title = Column(Text)
    completed = Column(Boolean)
