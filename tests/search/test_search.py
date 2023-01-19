URI = '/api/v1/search'
MOCK_DATA = [
    {'_id': '63c6f9461d1c19c5f2f01aaf', 'name': '경영평가관련 정보수집', 'code': 'SKILL#ee0501a0-f517-4ad7-985b-ad73c05ef261', 'highlights': [{'score': 1.1180211305618286, 'path': 'name', 'texts': [{'value': '경영평가관련 정보수집', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01ab0', 'name': '경영평가방법 설정', 'code': 'SKILL#17dde109-7ba8-453f-8fc2-21b067218c12', 'highlights': [{'score': 1.1151154041290283, 'path': 'name', 'texts': [{'value': '경영평가방법 설정', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01ab1', 'name': '경영평가도구 개발', 'code': 'SKILL#c3197d16-f9f7-45e1-ae42-3e0f8b6ab3d5', 'highlights': [{'score': 1.1151154041290283, 'path': 'name', 'texts': [{'value': '경영평가도구 개발', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01ab2', 'name': '경영평가활동 수행', 'code': 'SKILL#df4897fd-ebc5-4324-b440-47dbb0ba7501', 'highlights': [{'score': 1.1151154041290283, 'path': 'name', 'texts': [{'value': '경영평가활동 수행', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01ab3', 'name': '경영평가 결과 보고서 작성', 'code': 'SKILL#5919dd9e-f99e-47c5-ba68-9f75a79f3c40', 'highlights': [{'score': 0.9106559753417969, 'path': 'name', 'texts': [{'value': '경영평가 결과 보고서', 'type': 'hit'}, {'value': ' 작성', 'type': 'text'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01ab4', 'name': '경영평가 모니터링', 'code': 'SKILL#b22ecf75-5d27-41e0-9f76-16e7e54657b2', 'highlights': [{'score': 1.1151154041290283, 'path': 'name', 'texts': [{'value': '경영평가 모니터링', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01ab5', 'name': '경영평가 사후관리', 'code': 'SKILL#68bc655c-db40-4a84-aeac-77d64110427c', 'highlights': [{'score': 1.1151154041290283, 'path': 'name', 'texts': [{'value': '경영평가 사후관리', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01ab6', 'name': '경영평가계획 수립', 'code': 'SKILL#b80d975f-6ced-42bd-ae33-2d06891b44f5', 'highlights': [{'score': 1.1151154041290283, 'path': 'name', 'texts': [{'value': '경영평가계획 수립', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f04cde', 'name': '스마트양식 경영평가', 'code': 'SKILL#c6d2178b-2c66-4e33-97bf-75bea1a92c74', 'highlights': [{'score': 1.401990294456482, 'path': 'name', 'texts': [{'value': '스마트양식 ', 'type': 'text'}, {'value': '경영평가', 'type': 'hit'}]}]}
]


def test_pass(client, mock_search):
    ...
    # TODO: search Unittest
    #  mock_search.return_value = MOCK_DATA
    #
    #  res = client.get(f'{URI}?limit=10&query=test&type=ANY')
    #
    #  assert res.status_code == 200
    #  assert len(res.json()) == len(MOCK_DATA)
