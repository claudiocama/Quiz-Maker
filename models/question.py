# app/models/question.py

from pydantic import BaseModel
from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, JSON
from database import Base, engine

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)  # Specifica la lunghezza massima della stringa
    options = Column(JSON)
    correct_option = Column(Integer)
    
Base.metadata.create_all(bind=engine)


class QuestionBase(BaseModel):
    title: str
    options: List[str]
    correct_option: int

class QuestionUpdate(BaseModel):
    correct_option: int

