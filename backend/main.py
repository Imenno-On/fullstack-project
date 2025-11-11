from fastapi import FastAPI
from app.routes import health, tests

app = FastAPI(title="EduTest AI Backend")

# Подключаем маршруты
app.include_router(health.router)
app.include_router(tests.router)
