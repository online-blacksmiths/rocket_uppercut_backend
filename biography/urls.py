from fastapi import FastAPI, Depends

from common.config.consts import AUTH_HEADER

from biography.routes import set_img


def include_routers(app: FastAPI):
    app.include_router(set_img.router, tags=['Profile'], prefix='/api/v1/profile/img', dependencies=[Depends(AUTH_HEADER)])
