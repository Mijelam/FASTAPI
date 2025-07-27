from db.database import Base
from sqlalchemy import Column, Integer, String, Float


class Movie(Base):
    __tablename__ = "Movies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    overview = Column(String)
    rating = Column(Float)
    year = Column(Integer)
    category = Column(String)
