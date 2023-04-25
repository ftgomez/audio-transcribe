from fastapi import FastAPI
from data import GetItem, PostItem

app = FastAPI()

@app.post("/chat/{path}")
def create_chat(path):
    pass
