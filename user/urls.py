from fastapi import FastAPI

from user.routes import signup, verify, refresh


def include_routers(app: FastAPI):
    app.include_router(signup.router, tags=['회원가입'], prefix='/api/v1/user/signup')
    app.include_router(verify.router, tags=['인증'], prefix='/api/v1/user/verify')
    app.include_router(refresh.router, tags=['갱신'], prefix='/api/v1/user/refresh')
