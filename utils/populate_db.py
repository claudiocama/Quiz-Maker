from database import SessionLocal
from models.user import User
from models.question import Question
def populate_db():
    # Crea una sessione
    db = SessionLocal()
    # Inserisce gli utenti
    if db.query(User).count() == 0:
        users = [
            User(username="admin", password="admin", role="admin"),
            User(username="standard", password="standard", role="standard")
        ]
        db.add_all(users)
    
    # Inserisce le domande
    questions_data = [
        {
            "title": "Quale dei seguenti cicli \u00e8 adatto per eseguire un blocco di codice finch\u00e9 una condizione \u00e8 vera?",
            "options": [
                "if",
                "while",
                "for",
                "until"
            ],
            "correct_option": 1,
        },
        {
            "title": "Quale di queste variabili non \u00e8 valida in Python?",
            "options": [
                "my_variable",
                "2nd_variable",
                "_variable3",
                "variable_4"
            ],
            "correct_option": 1,
        },
        {
            "title": "Come si dichiara una lambda function in Python?",
            "options": [
                "function = lambda: x, y: x + y",
                "lambda x, y: x + y",
                "def lambda_function(x, y):",
                "lambda (x, y): x + y"
            ],
            "correct_option": 1,
        },
        {
            "title": "Come si definisce un costruttore in una classe Python?",
            "options": [
                "Utilizzando il metodo create().",
                "Definendo una funzione con il nome constructor.",
                "Utilizzando il metodo __init__.",
                "Dichiarando una funzione con qualsiasi nome."
            ],
            "correct_option": 2,
        },
        {
            "title": "Qual \u00e8 il risultato dell'espressione 5 // 2 in Python3?",
            "options": [
                "2",
                "2.5",
                "2.0",
                "2.25"
            ],
            "correct_option": 0,
        },
        {
            "title": "Quale istruzione Python consente di leggere l'input da un utente?",
            "options": [
                "input()",
                "get()",
                "read_input()",
                "user_input()"
            ],
            "correct_option": 0,
        },
        {
            "title": "Qual \u00e8 il risultato dell'espressione 10 == \"10\"?",
            "options": [
                "True",
                "False",
                "TypeError",
                "None"
            ],
            "correct_option": 1,
        }
    ]
    questions = [Question(**data) for data in questions_data]
    if db.query(Question).count() == 0:
        db.add_all(questions)
    
    # Commit delle modifiche
    db.commit()
    
    # Chiudi la sessione
    db.close()