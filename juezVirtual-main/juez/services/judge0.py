import requests

RAPIDAPI_HOST = "judge0-ce.p.rapidapi.com"
RAPIDAPI_KEY = "a39c9a6aeemshd842a65c7a7e82dp189890jsnaef825f77038"

SUBMISSION_URL = f"https://{RAPIDAPI_HOST}/submissions"

HEADERS = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST,
}

def submit_code(source_code, language_id, stdin=""):
    payload = {
        "source_code": source_code,
        "language_id": language_id,
        "stdin": stdin,
    }
    response = requests.post(SUBMISSION_URL, json=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_submission(token):
    url = f"{SUBMISSION_URL}/{token}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()
