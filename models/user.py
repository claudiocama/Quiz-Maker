from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, unique=True, index=True)
    role = Column(String)
    password = Column(String)
class UserLogin(BaseModel):
    username: str
    password: str
