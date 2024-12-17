from pydantic import BaseModel

class URLRequest(BaseModel):
    url: str

class ChatRequest(BaseModel):
    chat_id: str
    question: str
