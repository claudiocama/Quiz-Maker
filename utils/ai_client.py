import requests
import json
perplexity_api_key = ""


def explain_wrong_answer(question, wrong_answer, correct_answer):
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "Non superare le 30 parole e rispondi in italiano"
            },
            {
                "role": "user",
                "content": "Come mai la risposta corretta alla domanda '" + question + "' è '" + correct_answer + " e non " + wrong_answer + "'?"
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {perplexity_api_key}"
    }      
    response = requests.post(url, json=payload, headers=headers)
    response_json = json.loads(response.text)
    ai_explaination = response_json.get("choices")[0].get("message", {}).get("content", "")
    return ai_explaination