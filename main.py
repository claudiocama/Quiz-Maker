from fastapi import FastAPI, Request, HTTPException,  Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from datetime import timedelta

from routes import questions, quiz
from utils.populate_db import populate_db
from models.user import UserLogin
from utils.auth import authenticate_user, create_access_token

@asynccontextmanager
async def lifespan(app: FastAPI):
    #open connection
    populate_db()
    yield
    #close connection

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
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
async def login(response: Response, form_data: UserLogin):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=180)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token)

    return {"access_token": access_token}


@app.post("/logout")
async def logout(request: Request):
    response = templates.TemplateResponse("index.html", {"request": request})
    response.delete_cookie("access_token")
    return response