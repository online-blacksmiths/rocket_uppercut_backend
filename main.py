import uvicorn
from dataclasses import asdict
from redis_om import get_redis_connection
from redis import asyncio as aioredis

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.middleware.base import BaseHTTPMiddleware

from common.config.settings import conf
from common.config.rdb_conn import rdb
from common.config.mongodb_conn import mongodb

from common.utils.middlewares import request_middleware, access_control

from common.urls import include_routers as common_routers
from user.urls import include_routers as user_routers
from biography.urls import include_routers as biography_routers
from search.urls import include_routers as search_routers


def create_app():
    app = FastAPI()

    # RDB Connect
    rdb.init_app(app, **asdict(conf()))

    # MongoDB Connect
    mongodb()

    # Redis Connect
    get_redis_connection()

    redis = aioredis.from_url(conf().REDIS_URL, encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')

    # Middlewares
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=request_middleware)
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Endpoints
    search_routers(app)
    biography_routers(app)
    user_routers(app)
    common_routers(app)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=conf().PORT, reload=True)
