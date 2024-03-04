from fastapi import APIRouter, Request, HTTPException, status, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models.quiz import QuestionAnswer
from utils.json_utils import read_questions
from utils.random_utils import select_random_objects

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/quiz", response_class=HTMLResponse)
async def get_quiz(request: Request, question_count: int):
    questions = read_questions()
    quiz = select_random_objects(questions, question_count)
    return templates.TemplateResponse("quiz.html", {"request": request, "questions": quiz, "num_questions": len(quiz)})


@router.post("/quiz", response_class=HTMLResponse)
async def answer_question(question_answer: QuestionAnswer):
    for question in read_questions():
        if question["id"] == question_answer.question_id:
            selected_question = question
    
    if selected_question["correct_option"] == question_answer.answer:
        return Response(status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Risposta sbagliata",
        )
