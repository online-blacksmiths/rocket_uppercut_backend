URI = '/api/v1/search'
MOCK_DATA = [
    {'_id': '63c6f9461d1c19c5f2f01aa7', 'type': 'SKILL', 'code': 'SKILL#f2d45f78-8943-4b6e-83d9-fd086b6ac1ef', 'title': '경영방침 수립', 'highlights': [{'score': 1.1120877265930176, 'path': 'title', 'texts': [{'value': '경영방침 수립', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01aa8', 'type': 'SKILL', 'code': 'SKILL#62c0f4a8-a642-4a16-8335-96b46a2bb0f0', 'title': '경영계획 수립', 'highlights': [{'score': 1.1120877265930176, 'path': 'title', 'texts': [{'value': '경영계획 수립', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01aac', 'type': 'SKILL', 'code': 'SKILL#b8dcd72f-8f1b-45b3-830a-ccde54ccb4ea', 'title': '경영실적 분석', 'highlights': [{'score': 1.1120877265930176, 'path': 'title', 'texts': [{'value': '경영실적 분석', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01aad', 'type': 'SKILL', 'code': 'SKILL#2fffdec1-c1bc-4928-9255-3322eb4d0179', 'title': '경영 리스크 관리', 'highlights': [{'score': 0.8978784084320068, 'path': 'title', 'texts': [{'value': '경영 리스크 관리', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01aaf', 'type': 'SKILL', 'code': 'SKILL#ee0501a0-f517-4ad7-985b-ad73c05ef261', 'title': '경영평가관련 정 보수집', 'highlights': [{'score': 1.1180211305618286, 'path': 'title', 'texts': [{'value': '경영평가관련 정보수집', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01ab0', 'type': 'SKILL', 'code': 'SKILL#17dde109-7ba8-453f-8fc2-21b067218c12', 'title': '경영평가방법 설 정', 'highlights': [{'score': 1.1151154041290283, 'path': 'title', 'texts': [{'value': '경영평가방법 설정', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01ab1', 'type': 'SKILL', 'code': 'SKILL#c3197d16-f9f7-45e1-ae42-3e0f8b6ab3d5', 'title': '경영평가도구 개 발', 'highlights': [{'score': 1.1151154041290283, 'path': 'title', 'texts': [{'value': '경영평가도구 개발', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01ab2', 'type': 'SKILL', 'code': 'SKILL#df4897fd-ebc5-4324-b440-47dbb0ba7501', 'title': '경영평가활동 수 행', 'highlights': [{'score': 1.1151154041290283, 'path': 'title', 'texts': [{'value': '경영평가활동 수행', 'type': 'hit'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01ab3', 'type': 'SKILL', 'code': 'SKILL#5919dd9e-f99e-47c5-ba68-9f75a79f3c40', 'title': '경영평가 결과 보고서 작성', 'highlights': [{'score': 0.9106559753417969, 'path': 'title', 'texts': [{'value': '경영평가 결과 보고서', 'type': 'hit'}, {'value': ' 작성', 'type': 'text'}]}]},
    {'_id': '63c6f9461d1c19c5f2f01ab4', 'type': 'SKILL', 'code': 'SKILL#b22ecf75-5d27-41e0-9f76-16e7e54657b2', 'title': '경영평가 모니터 링', 'highlights': [{'score': 1.1151154041290283, 'path': 'title', 'texts': [{'value': '경영평가 모니터링', 'type': 'hit'}]}]}
]


def test_pass(client, mock_search):
    mock_search.return_value = MOCK_DATA

    res = client.get(f'{URI}?limit=10&query=test&type=ANY')

    assert res.status_code == 200
    assert len(res.json()) == len(MOCK_DATA)


def test_invalid_type(client, mock_search):
    mock_search.return_value = MOCK_DATA

    res = client.get(f'{URI}?limit=10&query=test&type=INVALID_TYPE')

    assert res.status_code == 422
