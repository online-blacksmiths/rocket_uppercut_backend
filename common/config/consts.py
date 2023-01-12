from fastapi.security import APIKeyHeader

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIMEZONE = "Asia/Seoul"
# 비밀번호 유효성 검증용 정규식 : 8자리 이상 + 숫자 + 특수문자
PASSWORD_REGEX = r'^(?=.*[\d])(?=.*[a-z|A-Z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
PHONE_VERIFY_CODE_REGEX = r'^[0-9]{6}$'
AUTH_HEADER = APIKeyHeader(name='Authorization', auto_error=False)
NCP_SENS_SMS_URL = 'https://sens.apigw.ntruss.com/sms/v2/services/{service_id}/messages'
NCP_OUTBOUND_MAILER_URL = 'https://mail.apigw.ntruss.com/api/v1/mails'
SMS_VERIFY_MSG = '[로켓 어퍼컷] 인증번호 [{verify_code}]를 입력해주세요.'

LOGIN_REQUIRED_PATH_LIST = [
    '/signin_test',
    '/api/v1/user/verify/phone',
    '/api/v1/user/verify/step'
]

LOGIN_REQUIRED_REGEX_PATH_LIST = [

]
