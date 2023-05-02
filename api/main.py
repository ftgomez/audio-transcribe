import os
import json
import random
from fastapi import FastAPI
from .data import GetItem, PostItem
from audio_transcribe import AudioTranscribe, QuestionBot

app = FastAPI()

@app.post('/create_chat')
def create_chat(item: PostItem):
    transcript = AudioTranscribe(item.path).transcribe()
    response = QuestionBot(transcript).answer_question(item.query)
    while True:
        chat_id = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(10)))
        if not os.path.isdir(chat_id):
            dicc = {
                'chat_id': chat_id,
                'transcript': transcript,
                'query': item.query,
                'response': response
            }
            os.mkdir(chat_id)
            with open(f'{chat_id}/0.json', 'w') as outfile:
                json.dump(dicc, outfile)

            return dicc
        
@app.get('chat/{chat_id}')
def chat(chat_id, item: GetItem):
    files = os.listdir(chat_id)
    files = list(filter(lambda x: '.json' in x, files))
    dicts = list(map(lambda x: open(x), files))
    querys = list(map(lambda x: json.load(x)['query'], dicts))
    querys.append(item.query)
    answers = list(map(lambda x: json.load(x)['response'], dicts))
    transcript = json.load(dicts[0]['transcript'])

    bot = QuestionBot(transcript)
    response = bot.auto_chat(querys, answers)
    
    dicc = {
        'chat_id': chat_id,
        'query': item.query,
        'response': response
    }

    chat_number = len(answers)
    with open(f'{chat_id}/{chat_number}.json', 'w') as outfile:
        json.dump(dicc, outfile)

    return dicc




