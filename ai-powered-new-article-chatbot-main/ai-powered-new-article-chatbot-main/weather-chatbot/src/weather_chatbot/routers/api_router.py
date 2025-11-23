from fastapi.routing import APIRouter
from src.weather_chatbot.routers.auth import router as auth_router
from src.weather_chatbot.routers.chatbot import router as chatbot_router
from src.weather_chatbot.routers.llm import router as llm_router

router = APIRouter()
router.include_router(auth_router, tags=["auth"])
router.include_router(chatbot_router, tags=["chatbot"])
router.include_router(llm_router, tags=["llm-config"])
