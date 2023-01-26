from pydantic.main import BaseModel

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder

from search.db.mongodb.documents import TotalSearch, TotalSearchEnum
from recruit.db.rdb.schema import Skill


router = APIRouter()


class SearchResponse(BaseModel):
    title: str
    code: str
    type: str


@router.get('', status_code=200, response_model=list[SearchResponse])
@cache(namespace='search', coder=JsonCoder, expire=30)
async def search(request: Request, type: TotalSearchEnum, limit: int = 10, query: str = ''):
    '''
    # Auther
    - [Yongineer1990](https://github.com/Yongineer1990)

    # Description
    - Search API

    # Query Params
    - limit: int = 최대 검색 갯수
        - default 10
    - type: str = 검색 타입
        - SKILL = 관심분야, 스킬
        - POSITION = 포지션
        - COMPANY = 회사
        - PEOPLE = 사람
        - RECRUIT = 채용
        - SCHOOL = 학교
        - MAJOR = 학과
        - ANY = 전체 검색 (단, 전체 검색에서 PEOPLE, COMPANY, RECRUIT 만 검색됨)
    - query: str = 검색어
        - default ""

    # Response
    - Array
    - title: str = 타이틀
    - code: str = 데이터 Key
    - type: str = 데이터 타입
    '''
    if query == '':
        return []

    pipeline = [
        {'$search': {'compound': {
            'filter': [{'text': {'query': query, 'path': 'title'}}],
            'must': [{'text': {'query': str(type), 'path': 'type'}}]
        }}},
        {'$limit': limit},
        {'$project': {'title': 1, 'code': 1, 'type': 1, 'score': {"$meta": "searchScore"}}}
    ]

    if type == TotalSearchEnum.ANY:
        pipeline[0]['$search']['compound']['must'] = [{
                'text': {'query': [str(TotalSearchEnum.PEOPLE), str(TotalSearchEnum.COMPANY), str(TotalSearchEnum.RECRUIT)],
                         'path': 'type'}
        }]
        pipeline.append({'$sort': {'total_sort': -1}})

    results = TotalSearch.objects().aggregate(pipeline=pipeline)

    return [dict(title=result['title'], code=result['code'], type=result['type']) for result in results]


class SkillSearchRequest(BaseModel):
    code: list[str] = []


@router.post('/skill', status_code=200, response_model=list[SearchResponse])
async def skill_search(request: Request, body: SkillSearchRequest, limit: int = 10):
    '''
    # Auther
    - [Yongineer1990](https://github.com/Yongineer1990)

    # Description
    - Skill Search API
    - 기존 선택된 스킬들과 연관이 있는 스킬들을 검색
    - request body 빈 배열 전달 시 기본 스킬들을 반환

    # Query Params
    - limit: int = 최대 검색 갯수
        - default 10

    # Request Body
    - code: array[str] = 기 선택된 스킬들의 코드 리스트
        - example
        - ["SKILL#916df4d4-db9b-416a-b678-824a46616045", "SKILL#9aa6417c-9773-46e3-98f3-25ad7b9a50c2"]

    # Response
    - Array
    - title: str = 타이틀
    - code: str = 데이터 Key
    - type: str = 데이터 타입
    '''
    if not body.code:
        return [dict(type=str(TotalSearchEnum.SKILL), **data)
                for data in await Skill.filter(is_initial = True).order_by('-id').values('title', 'code')]

    skills = await Skill.filter(code__in = body.code)

    if not skills:
        return []

    pipeline = [
        {'$search': {'compound': {
            'filter': [
                {'text': {'query': [skill.sub_title for skill in skills], 'path': 'sub_title'}},
            ],
            'must': [{'text': {'query': str(TotalSearchEnum.SKILL), 'path': 'type'}}],
            'mustNot': [{'text': {'query': [skill.title for skill in skills], 'path': 'title'}}]
        }}},
        {'$sample': {'size': limit}},
        {'$project': {'title': 1, 'code': 1, 'type': 1, 'score': {"$meta": "searchScore"}}}
    ]

    results = TotalSearch.objects().aggregate(pipeline=pipeline)

    return [dict(title=result['title'], code=result['code'], type=result['type']) for result in results]
