from fastapi import FastAPI
from .data import GetItem, PostItem

app = FastAPI()

@app.get("/chat/{path}")
def create_chat(path):
    return {
        'text': 'Hola mundo'
    }
