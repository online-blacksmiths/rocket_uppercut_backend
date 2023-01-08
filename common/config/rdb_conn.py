import sys
import logging

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from common.config.tortoise import TORTOISE_ORM


class RDBconnect:
    def __init__(self, app: FastAPI = None, **kwargs):
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI = None, **kwargs):
        is_test = kwargs.setdefault('TEST_MODE', False)
        is_debug = kwargs.setdefault('DEBUG', True)

        if is_test:
            register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True, add_exception_handlers=True)

        else:
            register_tortoise(app, config=TORTOISE_ORM, add_exception_handlers=True)

        if is_debug and not is_test:
            fmt = logging.Formatter(
                fmt = "%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            sh = logging.StreamHandler(sys.stdout)
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(fmt)

            logger_db_client = logging.getLogger('tortoise.db_client')
            logger_db_client.setLevel(logging.DEBUG)
            logger_db_client.addHandler(sh)

            logger_tortoise = logging.getLogger('tortoise')
            logger_tortoise.setLevel(logging.DEBUG)
            logger_tortoise.addHandler(sh)


rdb = RDBconnect()
