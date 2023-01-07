import uvicorn

from fastapi import FastAPI

from common.routes import index


def create_app():
    app = FastAPI()

    app.include_router(index.router, tags=['Health Check'], deprecated=True)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
