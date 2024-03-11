# app/routes/questions.py

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models.question import QuestionBase, QuestionUpdate
from utils.auth import check_token, check_is_admin
from database import SessionLocal
from models.question import Question


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/questions", response_class=HTMLResponse, dependencies=[Depends(check_token)])
async def index(request: Request):
    db = SessionLocal()
    questions = db.query(Question).all()
    db.close()
    return templates.TemplateResponse("questions.html", {"request": request, "questions": questions, "num_questions": len(questions)})


@router.post("/questions", response_class=HTMLResponse, dependencies=[Depends(check_is_admin)])
async def create_question(request: Request, questionBase: QuestionBase):
    db = SessionLocal()
    question = Question(title=questionBase.title, options=questionBase.options, correct_option=questionBase.correct_option)
    db.add(question)
    db.commit()
    questions = db.query(Question).all()
    db.close()
    return templates.TemplateResponse("questions.html", {"request": request, "questions": questions, "num_questions": len(questions)})


@router.put("/questions/{question_id}", response_class=HTMLResponse, dependencies=[Depends(check_is_admin)])
async def update_question(request: Request, question_id: int, question_update: QuestionUpdate):
    db = SessionLocal()
    question = db.query(Question).filter_by(id=question_id).first()   
    if question:
        question.correct_option = question_update.correct_option
        db.commit()
    questions = db.query(Question).all()
    db.close()
    return templates.TemplateResponse("questions.html", {"request": request, "questions": questions, "num_questions": len(questions)})


@router.delete("/questions/{question_id}", response_class=HTMLResponse, dependencies=[Depends(check_is_admin)])
async def delete_question(request: Request, question_id: int):
    db = SessionLocal()
    question = db.query(Question).filter_by(id=question_id).first()
    if question:
        db.delete(question)
        db.commit()
    questions = db.query(Question).all()
    db.close()
    return templates.TemplateResponse("questions.html", {"request": request, "questions": questions, "num_questions": len(questions)})