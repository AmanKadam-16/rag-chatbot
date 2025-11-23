from src.weather_chatbot.schemas.user import AddUser, UserResponse
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.weather_chatbot.models.base import WeatherAppUser
from src.weather_chatbot.services.auth import hash_password, verify_password


def add_user(user_data: AddUser, db: Session) -> UserResponse:
    user_info = (
        db.query(WeatherAppUser)
        .filter(WeatherAppUser.user_email == user_data.user_email)
        .first()
    )

    if user_info:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists.",
        )
    hashed_password = hash_password(user_data.password)
    new_user = WeatherAppUser(
        user_email=user_data.user_email, hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(user_data: AddUser, db: Session) -> UserResponse:
    user_info = (
        db.query(WeatherAppUser)
        .filter(WeatherAppUser.user_email == user_data.user_email)
        .first()
    )
    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    if not verify_password(user_data.password, user_info.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    return user_info
