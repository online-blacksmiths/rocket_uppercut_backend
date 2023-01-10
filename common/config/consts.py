from fastapi.security import APIKeyHeader

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIMEZONE = "Asia/Seoul"
# 비밀번호 유효성 검증용 정규식 : 8자리 이상 + 숫자 + 특수문자
PASSWORD_REGEX = r'^(?=.*[\d])(?=.*[a-z|A-Z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
AUTH_HEADER = APIKeyHeader(name='Authorization', auto_error=False)

LOGIN_REQUIRED_PATH_LIST = [
    '/signin_test'
]

LOGIN_REQUIRED_REGEX_PATH_LIST = [

]
