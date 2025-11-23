from pydantic import BaseModel
from enum import Enum
from uuid import UUID


class ChatRole(Enum):
    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"


class UserInput(BaseModel):
    content: str


"""
class WeatherAppChatHistory(Base):
    __tablename__ = "chathistory"
    chat_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(ForeignKey("userinfo.id"))
    role = Column(String, nullable=False, index=True)  # user / assistant
    chat_message = Column(String)
    created_at = Column(DateTime, nullable=False, default=func.now())
"""


class ChatMessage(BaseModel):
    role: ChatRole
    content: str


class ChatLog(BaseModel):
    role: ChatRole
    chat_message: str


class ChatLogHistory(ChatLog):
    # session_id: UUID
    ...


class ChatHistory(ChatMessage):
    session_id: str
    user_id: int


class RetrieveChatHistory(BaseModel):
    session_id: str
    user_id: int
    conversations: list[ChatMessage]
