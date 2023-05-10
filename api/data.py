from pydantic import BaseModel

class PostCreateItem(BaseModel):
    path: str
    query: str

class PostAskItem(BaseModel):
    query: str