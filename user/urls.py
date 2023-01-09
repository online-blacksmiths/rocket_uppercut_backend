from fastapi import FastAPI

from user.routes import signup


def include_routers(app: FastAPI):
    app.include_router(signup.router, tags=['Signup'], prefix='/api/v1/signup')
