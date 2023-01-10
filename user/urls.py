from fastapi import FastAPI

from user.routes import signup, verify


def include_routers(app: FastAPI):
    app.include_router(signup.router, tags=['회원가입'], prefix='/api/v1/signup')
    app.include_router(verify.router, tags=['인증'], prefix='/api/v1/verify')
