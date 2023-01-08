import uvicorn
from dataclasses import asdict

from fastapi import FastAPI

from common.config.settings import conf
from common.config.rdb_conn import rdb
from common.config.mongodb_conn import mongodb
from common.routes import index


def create_app():
    app = FastAPI()

    # RDB Connect
    rdb.init_app(app, **asdict(conf()))

    # MongoDB Connect
    mongodb()

    app.include_router(index.router, tags=['Health Check'], deprecated=True)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
