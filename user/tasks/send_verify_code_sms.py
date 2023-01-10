import httpx
import asyncio

from loguru import logger
import phonenumbers

from user.utils.token import Method, get_ncp_signature
from user.db.rdb.schema import User

from common.config.settings import conf
from common.config.consts import NCP_SENS_SMS_URL, SMS_VERIFY_MSG


async def request(client, user: User, verify_code: str):
    phone = phonenumbers.parse(user.phone)

    url = NCP_SENS_SMS_URL.format(service_id = conf().NCP_SENS_SERVICE_ID)
    timestamp, signature = get_ncp_signature(method=Method.POST, url=url)

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': conf().NCP_ACCESS_KEY,
        'x-ncp-apigw-signature-v2': signature
    }

    body = {
        'type' : 'SMS',
        'countryCode' : str(phone.country_code),
        'from': '01025201513',
        'content' : SMS_VERIFY_MSG.format(verify_code = verify_code),
        'messages' : [{'to': str(phone.national_number)}]
    }

    res = await client.post(url=url, headers=headers, json=body)

    return res.json()


async def task(user: User, verify_code: str):
    async with httpx.AsyncClient() as client:
        task = request(client, user=user, verify_code=verify_code)
        result = await asyncio.gather(task)

        logger.info(result)
