from fastapi.routing import APIRouter
from src.weather_chatbot.services.auth import get_current_user
from src.weather_chatbot.schemas.chatbot import UserInput, ChatLogHistory
from src.weather_chatbot.services.chatbot import (
    chat_with_llm,
    retrieve_chat_history,
    get_mock_llm_responses,
)
from fastapi import Depends, HTTPException

router = APIRouter(prefix="/chatbot")


@router.post("/conversation/{session_id}")
def chat(user_input: UserInput, session_id: str, user_id=Depends(get_current_user)):
    try:
        response = chat_with_llm(
            user_input=user_input, session_id=session_id, user_id=user_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")


@router.get("/conversation/{session_id}", response_model=list[ChatLogHistory])
def get_chat(session_id: str, user_id=Depends(get_current_user)):
    try:
        chat_history = retrieve_chat_history(session_id=session_id, user_id=user_id)
        return chat_history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")


@router.post("/mock-conversation/{session_id}")
def mock_chat(
    user_input: UserInput, session_id: str, user_id=Depends(get_current_user)
):
    try:
        response = get_mock_llm_responses(user_prompt=user_input, session_id=session_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")
