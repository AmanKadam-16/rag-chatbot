from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.weather_chatbot.core.config import settings
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

TOKEN_EXPIRY_TIME = settings.TOKEN_EXPIRE_MINUTES
APP_SECRET = settings.SECRET
ALGORITHM = settings.JWT_ALGORITHM

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")
security = HTTPBearer()


def hash_password(plain_password):
    hashed_password = pwd_context.hash(plain_password)
    return hashed_password


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def create_token(data: dict):
    payload_claims = data.copy()
    token_expire_at = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRY_TIME)
    token_expiry = {"exp": token_expire_at}
    payload_claims.update(token_expiry)
    jwt_token = jwt.encode(claims=payload_claims, key=APP_SECRET, algorithm=ALGORITHM)
    return jwt_token


def validate_token(token):
    try:
        payload = jwt.decode(token=token, key=APP_SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Error : {e}"
        )


def get_current_user(credential: HTTPAuthorizationCredentials = Depends(security)):
    token = credential.credentials
    payload_claims = validate_token(token)
    user_id = payload_claims.get("sub")
    return user_id
