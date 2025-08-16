# Pydantic models for request/response
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    user_id: str

class GeminiResponse(BaseModel):
    answer: str


    