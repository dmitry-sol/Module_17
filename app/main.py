from fastapi import FastAPI
from app.routers import user, task

api = FastAPI()

api.include_router(user.router)
api.include_router(task.router)

@api.get('/')
async def root():
    return {"message": "Welcome to Taskmanager"}



# pipreqs
# python -m uvicorn app.main:api --reload

