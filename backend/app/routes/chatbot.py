from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.chatbot import ChatRequest, ChatResponse
from app.utils.dependencies import get_current_user, get_db
from app.services.chatbot_service import handle_chat


router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("/ask", response_model=ChatResponse)
def chat_with_bot(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    reply = handle_chat(data.message, db, current_user)

    return {"reply": reply}