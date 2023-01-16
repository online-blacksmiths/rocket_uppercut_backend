from fastapi import FastAPI, Depends

from common.config.consts import AUTH_HEADER

from user.routes import signup, verify_phone, refresh, steps, verify_email, signin, me


def include_routers(app: FastAPI):
    app.include_router(signup.router, tags=['회원가입'], prefix='/api/v1/user/signup')
    app.include_router(verify_phone.router, tags=['인증 : 휴대폰', '인증'], prefix='/api/v1/user/verify/phone', dependencies=[Depends(AUTH_HEADER)])
    app.include_router(verify_email.router, tags=['인증 : 이메일', '인증'], prefix='/api/v1/user/verify/email')
    app.include_router(steps.router, tags=['인증'], prefix='/api/v1/user/verify/step', dependencies=[Depends(AUTH_HEADER)])
    app.include_router(refresh.router, tags=['갱신'], prefix='/api/v1/user/refresh')
    app.include_router(signin.router, tags=['로그인'], prefix='/api/v1/user/signin')
    app.include_router(me.router, tags=['내 정보'], prefix='/api/v1/user/me', dependencies=[Depends(AUTH_HEADER)])
