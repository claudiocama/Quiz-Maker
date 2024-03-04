# app/routes/questions.py

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models.question import QuestionBase, QuestionUpdate
from utils.json_utils import read_questions, write_questions
from utils.random_utils import generate_random_id

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/questions", response_class=HTMLResponse)
async def create_question(request: Request, question: QuestionBase):
    questions_db = read_questions()
    question_dict = question.model_dump()
    question_dict["id"] = generate_random_id()

    questions_db.append(question_dict)
    write_questions(questions_db)
    return templates.TemplateResponse("index.html", {"request": request, "questions": questions_db, "num_questions": len(questions_db)})


@router.put("/questions/{question_index}", response_class=HTMLResponse)
async def update_question(request: Request, question_index: int, question_update: QuestionUpdate):
    questions_db = read_questions()
    questions_db[question_index]["correct_option"] = question_update.correct_option
    write_questions(questions_db)
    return templates.TemplateResponse("index.html", {"request": request, "questions": questions_db, "num_questions": len(questions_db)})


@router.delete("/questions/{question_index}", response_class=HTMLResponse)
async def delete_question(request: Request, question_index: int):
    questions_db = read_questions()
    questions_db.pop(question_index)
    write_questions(questions_db)
    return templates.TemplateResponse("index.html", {"request": request, "questions": questions_db, "num_questions": len(questions_db)})