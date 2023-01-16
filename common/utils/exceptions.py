from common.db.rdb.schema import Error


async def exception_handler(error: Exception):
    if not isinstance(error, APIException):
        error = APIException(exception=error, detail=str(error))

    return error


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


class SignInError(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


class ImageUploadError(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


class DuplicatedUser(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


class VerifyMsgNotFound(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


class StepNotFound(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


class LoginRequire(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


class UserNotFound(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


class InvalidData(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


class InvalidPhoneNumber(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


class SignupException(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


class TokenExpired(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


class TokenDecodeError(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )


class TooManyRequestVerify(APIException):
    def __init__(self, e: Error, exception: Exception = None):
        super().__init__(
            status_code=e.status_code, msg=e.msg, detail=e.detail, code=e.code, exception=exception
        )
