from fastapi import FastAPI, APIRouter

from app.api import auth, project, task

app = FastAPI(
    title="Todo List API",
    description="Backend для Todo List с JWT авторизацией, проектами и задачами",
    version="1.0.0"
)

api_v1 = APIRouter(prefix="/v1")
api_v1.include_router(auth.router)
api_v1.include_router(project.router)
api_v1.include_router(task.router)

app.include_router(api_v1)

