from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.utils.gemini_client import ask_gemini
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/ask", response_model=ChatResponse)
def chat_with_bot(
    data: ChatRequest,
    current_user=Depends(get_current_user)
):
    """
    Chatbot endpoint for students
    """
    reply = ask_gemini(data.message)
    return {"reply": reply}
