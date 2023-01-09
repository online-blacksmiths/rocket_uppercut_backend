from phonenumbers import phonenumberutil, is_valid_number, parse as phonenumber_parser

from common.db.rdb.schema import Error
from common.utils.excetions import InvalidPhoneNumber

from user.db.rdb.schema import User


async def valid_phone(phone: str) -> str:
    try:
        phonenumber = phonenumber_parser(phone)

        if not is_valid_number(phonenumber):
            e = await Error.get(code='4000002')
            raise InvalidPhoneNumber(e=e)

        phone = f'+{phonenumber.country_code}{phonenumber.national_number}'

        if await User.filter(phone=phone).exists():
            e = await Error.get(code='4000003')
            raise InvalidPhoneNumber(e=e)

        return phone

    except phonenumberutil.NumberParseException:
        e = await Error.get(code='4000002')
        raise InvalidPhoneNumber(e=e)
