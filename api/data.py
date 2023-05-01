from pydantic import BaseModel

class PostItem(BaseModel):
    path: str
    query: str

class GetItem(BaseModel):
    query: str