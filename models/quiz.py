# app/models/quiz.py
from pydantic import BaseModel


class QuestionAnswer(BaseModel):
    question_id: str
    answer: int