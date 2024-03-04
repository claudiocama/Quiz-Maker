function updateCorrectOption(questionIndex, correctOption) {
    fetch('/questions/' + questionIndex, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            correct_option: correctOption
        }),
    }).then(() => {
        location.reload()
    })

}
function submitForm() {
    var form = document.getElementById("add-question-form");
    var formData = new FormData(form);
    var jsonData = {};
    formData.forEach(function (value, key) {
        if (key === 'options[]') {
            if (!jsonData.hasOwnProperty('options')) {
                jsonData['options'] = [];
            }
            jsonData['options'].push(value);
        } else {
            jsonData[key] = value;
        }
    });

    fetch('/questions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData),
    })
        .then(data => location.reload())
}

function deleteQuestion(questionIndex) {
    fetch(`/questions/${questionIndex}`, {
        method: 'DELETE'
    }).then(() => {
        location.reload();
    });
}

function generateQuiz() {
    const question_count = document.getElementById('question_count').value
    if (!question_count) {
        alert('Inserisci il numero di domande')
        return
    }
    document.location = "/quiz?question_count=" + question_count
}

function answerQuizQuestion(question_id, selected_answer) {
    fetch('/quiz', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_id: question_id,
            answer: selected_answer
        }),
    }).then((response) => {
        if (response.status == 200) {
            alert("Risposta corretta!");
        } else {
            alert("Risposta sbagliata, riprova");
        }
    });
}