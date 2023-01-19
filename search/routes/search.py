from pydantic.main import BaseModel

from fastapi import APIRouter
from fastapi.requests import Request

from search.db.mongodb.documents import TotalSearch, TotalSearchEnum


router = APIRouter()


class SearchResponse(BaseModel):
    title: str
    code: str
    type: str


@router.get('', status_code=200, response_model=list[SearchResponse])
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
        - ANY = 전체 검색 (단, 전체 검색에서 PEOPLE, COMPANY, RECRUIT 만 검색됨)
    - query: str = 검색어
        - default ""

    # Response
    - Array
    - title: str = 타이틀
    - code: str = 데이터 Key
    - type: str = 데이터 타입
    '''
    pipeline = [
        {'$search': {'compound': {'filter': [{'autocomplete': {'query': query, 'path': 'title'}}],
                                  'must': [{'text': {'query': str(type), 'path': 'type'}}]},
                     "highlight": {"path": "title"}}},
        {'$limit': limit},
        {'$project': {'title': 1, 'code': 1, 'type': 1, 'highlights': {"$meta": "searchHighlights"}}}
    ]

    if type == TotalSearchEnum.ANY:
        pipeline[0]['$search']['compound']['must'] = [{
                'text': {'query': [str(TotalSearchEnum.PEOPLE), str(TotalSearchEnum.COMPANY), str(TotalSearchEnum.RECRUIT)],
                         'path': 'type'}
        }]
        pipeline.append({'$sort': {'total_sort': -1}})

    results = TotalSearch.objects().aggregate(pipeline=pipeline)

    return [dict(title=result['title'], code=result['code'], type=result['type']) for result in results]
