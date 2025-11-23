from fastapi.routing import APIRouter
from src.weather_chatbot.services.auth import get_current_user
from src.weather_chatbot.services.chatbot import get_model_cards, update_model_preset
from fastapi import Depends, HTTPException

router = APIRouter(prefix="/model")


@router.post("/config", dependencies=[Depends(get_current_user)])
def activate_model(model_name: str):
    try:
        response = update_model_preset(model_name=model_name)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")


@router.get("/list", dependencies=[Depends(get_current_user)])
def get_models():
    try:
        models_list = get_model_cards()
        return models_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")
