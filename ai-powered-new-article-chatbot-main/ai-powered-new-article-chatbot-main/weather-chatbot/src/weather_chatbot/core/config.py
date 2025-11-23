from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    API_KEY: str
    API_BASE_URL: str
    DATABASE_URL: str
    TOKEN_EXPIRE_MINUTES: int
    SECRET: str
    JWT_ALGORITHM: str
    MODEL_CONTEXT_WINDOW: int = 4048
    MODEL_NAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Setting()
