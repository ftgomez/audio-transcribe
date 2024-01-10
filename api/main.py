import json
import os
import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from audio_transcribe import AudioTranscribe, QuestionBot

from .data import PostAskItem, PostCreateItem

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create_chat")
def create_chat(item: PostCreateItem):
    transcript = AudioTranscribe(item.path).transcribe()
    response = QuestionBot(transcript).answer_question(item.query)
    while True:
        chat_id = "".join(
            (random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(10))
        )
        if not os.path.isdir(chat_id):
            dicc = {
                "chat_id": chat_id,
                "transcript": transcript,
                "query": item.query,
                "response": response,
            }
            os.mkdir(chat_id)
            with open(f"{chat_id}/0.json", "w") as outfile:
                json.dump(dicc, outfile)

            return dicc


@app.post("/chat/{chat_id}")
def chat(chat_id, item: PostAskItem):
    files = os.listdir(chat_id)
    files = list(filter(lambda x: ".json" in x, files))
    files = sorted(files, key=get_number)
    files = list(map(lambda x: f"{chat_id}/{x}", files))
    dicts = list(map(lambda x: open(x), files))
    querys = list(map(lambda x: json.load(x)["query"], dicts))

    querys.append(item.query)

    with open(files[0], "r") as f:
        data = json.load(f)

    transcript = data["transcript"]
    bot = QuestionBot(transcript)
    response = bot.auto_chat(querys)

    dicc = {"chat_id": chat_id, "query": item.query, "response": response}

    chat_number = len(querys) - 1
    with open(f"{chat_id}/{chat_number}.json", "w") as outfile:
        json.dump(dicc, outfile)

    return dicc


def get_number(filename):
    return int(filename.split(".")[0])
