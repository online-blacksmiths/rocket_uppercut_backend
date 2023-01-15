import os
from synology_api import filestation

from PIL import Image

from fastapi import APIRouter, UploadFile
from fastapi.requests import Request

from common.db.rdb.schema import Error
from common.models import ResponseOK
from common.config.settings import conf
from common.config.consts import PROFILE_TEMP_PATH, PROFILE_IMAGE_PATH, PROFILE_IMG_EXTENSIONS
from common.utils.exceptions import ImageUploadError


router = APIRouter()

if not conf().TEST_MODE:
    fl = filestation.FileStation(conf().FILE_SERVER_IP, conf().FILE_SERVER_PORT, conf().FILE_SERVER_USER, conf().FILE_SERVER_PW, dsm_version=6)


@router.post('', status_code=201, summary='프로필 이미지 등록 API', response_model=ResponseOK)
async def upload_profile_img(request: Request, file: UploadFile):
    '''
    # Auther
    - [Yongineer1990](https://github.com/Yongineer1990)

    # Description
    - 프로필 이미지 등록 API
    - 로그인 필요 (Headers.Authorization)

    # Error
    - 4000008 : 이미지 크기가 200x200을 초과함
    - 4000009 : 이미지 업로드 실패
    - 4000010 : 이미지 형식이 jpg, jpeg, png, gif가 아님

    # Request
    - file
        - ex) file=@{file_path};type={media_type}
        - media_type은 생략해도 무방
        - [Media Type](https://developer.mozilla.org/ko/docs/Web/HTTP/Basics_of_HTTP/MIME_types)
    '''
    user = request.state.user

    extension = file.filename.split('.')[-1]
    if extension not in PROFILE_IMG_EXTENSIONS:
        e = await Error.get(code='4000010')
        raise ImageUploadError(e=e)

    file_location = f'{PROFILE_TEMP_PATH}/{user.user_key}.{extension}'

    with open(file_location, 'wb+') as file_obj:
        file_obj.write(await file.read())

    img = Image.open(file_location)

    if 200 < img.width or 200 < img.height:
        if os.path.isfile(file_location):
            os.remove(file_location)
        e = await Error.get(code='4000008')
        raise ImageUploadError(e=e)

    try:
        if not conf().TEST_MODE:
            fl.upload_file(file_path=file_location, dest_path=PROFILE_IMAGE_PATH)
            files = fl.get_file_list(PROFILE_IMAGE_PATH)['data']['files']
            if f'{user.user_key}.{extension}' not in [file['name'] for file in files]:
                e = await Error.get(code='4000009')
                raise ImageUploadError(e=e)

    except FileNotFoundError:
        e = await Error.get(code='4000009')
        raise ImageUploadError(e=e)

    if os.path.isfile(file_location):
        os.remove(file_location)

    user.profile_img_url = f'{conf().FILE_SERVER_URL}/{PROFILE_IMAGE_PATH.replace("/web/", "")}/{user.user_key}.{extension}'
    await user.save()

    return ResponseOK()
