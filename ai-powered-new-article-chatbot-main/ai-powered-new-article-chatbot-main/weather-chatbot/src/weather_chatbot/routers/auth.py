from fastapi.routing import APIRouter
from fastapi import HTTPException, status
from src.weather_chatbot.schemas.user import AddUser, UserResponse, UserLogin
from src.weather_chatbot.services import user as user_service
from src.weather_chatbot.services import auth as auth_service
from src.weather_chatbot.database.database import get_db
from fastapi import Depends

router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=UserResponse)
def register_user(user_credentials: AddUser, db=Depends(get_db)):
    try:
        response = user_service.add_user(user_data=user_credentials, db=db)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error : {e}"
        )


@router.post("/signin", response_model=UserLogin)
def login_user(user_credential: AddUser, db=Depends(get_db)):
    try:
        user_info = user_service.get_user(user_data=user_credential, db=db)
        initial_claim = {"sub": str(user_info.id)}
        access_token = auth_service.create_token(initial_claim)
        response = UserLogin(token=access_token)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error : {e}"
        )


@router.get("/me", dependencies=[Depends(auth_service.get_current_user)])
def check():
    return {"status": "200 OK"}
