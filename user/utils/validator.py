import ipaddress

from phonenumbers import phonenumberutil, is_valid_number, parse as phonenumber_parser
from email_validator import validate_email

from fastapi.requests import Request

from common.db.rdb.schema import Error
from common.utils.exceptions import InvalidPhoneNumber, DuplicatedUser, SignInError

from user.db.rdb.schema import User, SnsTypeEnum
from user.utils.get_info import get_ip, get_country_code


async def valid_phone(phone: str) -> str:
    try:
        phonenumber = phonenumber_parser(phone)

        if not is_valid_number(phonenumber):
            e = await Error.get(code='4000002')
            raise InvalidPhoneNumber(e=e)

        phone = f'+{phonenumber.country_code}{phonenumber.national_number}'

        if await User.filter(phone=phone).exists():
            e = await Error.get(code='4000003')
            raise DuplicatedUser(e=e)

        return phone

    except phonenumberutil.NumberParseException:
        e = await Error.get(code='4000002')
        raise InvalidPhoneNumber(e=e)


async def get_user_type(request: Request, ci: str) -> tuple[SnsTypeEnum, str]:
    try:
        email = validate_email(ci, check_deliverability=True).email

        return SnsTypeEnum.EMAIL, email

    except Exception:
        try:
            if not ci.isdigit():
                e = await Error.get(code='4010005')
                raise SignInError(e=e)

            ip = request.state.ip

            if not ip_validator(ip):
                ip = get_ip()

            country_code = get_country_code(ip=ip)
            phonenumber = phonenumber_parser(ci, country_code)

            return SnsTypeEnum.PHONE, f'+{phonenumber.country_code}{phonenumber.national_number}'

        except Exception:
            e = await Error.get(code='4010005')
            raise SignInError(e=e)


def ip_validator(ip: str) -> bool:
    try:
        PRIVATE_IP_LIST = ['10.0', '172.16', '192.168']
        if ip == '127.0.0.1' or '.'.join(ip.split('.')[:2]) in PRIVATE_IP_LIST:
            return False

        ipaddress.ip_address(ip)
        return True

    except ValueError:
        return False
