from pydantic import BaseModel, EmailStr, Field


class UserBaseModel(BaseModel):
    user_email: EmailStr

    class Config:
        from_attributes: True


class AddUser(UserBaseModel):
    password: str


class UserResponse(UserBaseModel):
    id: int


class UserLogin(BaseModel):
    token: str
    token_type: str = Field(default="bearer")
