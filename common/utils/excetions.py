from common.db.rdb.schema import Error


class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str
    exception: Exception

    def __init__(
        self,
        *,
        status_code: int = 500,
        code: str = "5000000",
        msg: str = '서버 오류',
        detail: str = 'Internal Server Error',
        exception: Exception = None
    ):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.detail = detail
        self.exception = exception

        super().__init__(exception)


class InvalidData(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


async def exception_handler(error: Exception):
    if not isinstance(error, APIException):
        error = APIException(exception=error, detail=str(error))

    return error
