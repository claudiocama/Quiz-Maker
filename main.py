from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routes import questions, quiz
from utils.json_utils import read_questions

app = FastAPI()

# Carica i template dalla directory 'templates'
templates = Jinja2Templates(directory="templates")
# Monta i file statici dalla directory 'static' in /static
app.mount("/static", StaticFiles(directory="static"), name="static")
# Monta i router per le domande e i quiz
app.include_router(questions.router)
app.include_router(quiz.router)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    questions_db = read_questions()
    return templates.TemplateResponse("index.html", {"request": request, "questions": questions_db, "num_questions": len(questions_db)})
