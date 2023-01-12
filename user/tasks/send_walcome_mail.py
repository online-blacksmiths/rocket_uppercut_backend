import codecs
import httpx
import asyncio

from loguru import logger

from user.utils.token import Method, get_ncp_signature
from user.db.rdb.schema import User

from common.config.settings import conf, base_dir
from common.config.consts import NCP_OUTBOUND_MAILER_URL


async def request(client, user: User):
    f = codecs.open(f'{base_dir}/templates/user/welcome.html', 'r')
    body = f.read().format(
        name=f'{user.first_name}{user.last_name}',
        profile_url='https://google.com',
        company_url='https://google.com',
        recruit_url='https://google.com'
    )

    timestamp, signature = get_ncp_signature(method=Method.POST, url=NCP_OUTBOUND_MAILER_URL)

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': conf().NCP_ACCESS_KEY,
        'x-ncp-apigw-signature-v2': signature
    }

    body = {
        'senderAddress' : 'no-reply@rocket-uppercut.com',
        'senderName' : 'RocketUppercut',
        'title': f'{user.first_name}{user.last_name} 님, 로켓 어퍼컷에 오신 것을 환영합니다. 🚀',
        'body' : body,
        'recipients' : [{'address': user.email, 'type': 'R'}]
    }

    res = await client.post(url=NCP_OUTBOUND_MAILER_URL, headers=headers, json=body)

    return res.json()


async def task(user: User):
    async with httpx.AsyncClient() as client:
        task = request(client, user=user)
        result = await asyncio.gather(task)

        logger.info(result)
