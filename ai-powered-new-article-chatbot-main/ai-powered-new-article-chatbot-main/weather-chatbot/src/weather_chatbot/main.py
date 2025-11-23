from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.weather_chatbot.routers.api_router import router

app = FastAPI(title="AI-Powered-Weather-Article-Chatbot")
app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def home():
    response_template = """
    <h1><a href="/docs">Swagger Docs</a></h1>
    <h1><a href="/redoc">Redocs</a></h1>
    """
    return response_template
