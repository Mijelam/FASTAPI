from db.database import Base
from sqlalchemy  import Column,Integer,String

class User(Base):
    __tablename__="User"
    id=Column(Integer,primary_key=True,autoincrement=True)
    email=Column(String,unique=True,index=True)
    password=Column(String)