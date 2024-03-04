import json

# Path del file JSON
questions_file = "questions.json"


def read_questions():
    with open(questions_file, "r") as file:
        return json.load(file)


def write_questions(questions):
    with open(questions_file, "w") as file:
        json.dump(questions, file, indent=4)
   
