from fastapi import APIRouter, Request, HTTPException, status, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models.quiz import QuestionAnswer
from utils.random_utils import select_random_objects
from utils.ai_client import explain_wrong_answer
from database import SessionLocal
from models.question import Question
router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/quiz", response_class=HTMLResponse)
async def get_quiz(request: Request, question_count: int):
    db = SessionLocal()
    questions = db.query(Question).all()
    db.close()
    quiz = select_random_objects(questions, question_count)
    return templates.TemplateResponse("quiz.html", {"request": request, "questions": quiz, "num_questions": len(quiz)})


@router.post("/quiz", response_class=HTMLResponse)
async def answer_question(question_answer: QuestionAnswer):
    db = SessionLocal()
    selected_question = db.query(Question).filter_by(id= question_answer.question_id).first()
    
    db.close()
    
    if selected_question.correct_option == question_answer.answer:
        return Response(status_code=status.HTTP_200_OK)
    
    title = selected_question.title
    correct_answer = selected_question.options[selected_question.correct_option]
    wrong_answer = selected_question.options[question_answer.answer]
    message = explain_wrong_answer(title, wrong_answer, correct_answer)
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )