from sqlalchemy import Column, String, Integer, DateTime, func, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from src.weather_chatbot.database.database import Base


class WeatherAppUser(Base):
    __tablename__ = "userinfo"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False, index=True)


class WeatherAppChatHistory(Base):
    __tablename__ = "chathistory"
    chat_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(ForeignKey("userinfo.id"))
    role = Column(String, nullable=False, index=True)  # user / assistant
    chat_message = Column(String)
    created_at = Column(DateTime, nullable=False, default=func.now())


class ContinentWeatherData(Base):
    __tablename__ = "continentweatherinfo"
    id = Column(Integer, primary_key=True, index=True)
    continent_name = Column(String, nullable=False, index=True)
    weather_metadata = Column(JSONB, nullable=True, index=True)
