from fastapi import FastAPI
from app.api.v1 import routes_auth, routes_tasks

app = FastAPI()

app.include_router(routes_auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(routes_tasks.router, prefix='/api/v1/tasks', tags=["tasks"])