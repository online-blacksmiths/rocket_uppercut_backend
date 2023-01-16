import httpx

from common.config.consts import GET_IP_URL, GET_NATIONAL_CODE_URL


def get_ip() -> str:
    res = httpx.get(GET_IP_URL)
    print(res)

    return res.text


def get_country_code(ip: str) -> str:
    res = httpx.get(GET_NATIONAL_CODE_URL.format(ip=ip))

    return res.json()['country']
