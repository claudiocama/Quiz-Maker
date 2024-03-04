# app/models/question.py

from pydantic import BaseModel
from typing import List


class QuestionBase(BaseModel):
    title: str
    options: List[str]
    correct_option: int

class QuestionUpdate(BaseModel):
    correct_option: int

