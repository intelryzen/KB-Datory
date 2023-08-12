import random
from fastapi import APIRouter
from fastapi import File, Form, UploadFile
from control.file_control import FileController
from control.db_control import DbController
from control.whisper_control import WhisperController
from mysql.manager.spam_manager import SpamManager
from config import *

api_router = APIRouter(
    prefix="/api",
    tags=["API"],
)

# 클라이언트가 15초마다 위 api 를 요청


@api_router.post("/score/")
async def get_score(target_phone: str = Form(...), my_phone: str = Form(...), file: UploadFile = File(...),):

    # 클라이언트로부터 받아온 wav (약 15 초) 파일 읽기
    file_name = file.filename
    file_contents = await file.read()

    # 서버에 파일을 저장하는 모듈 (서버에 파일이 이미 있다면 뒤에 이어붙이기)
    FileController.save_file(file_name, file_contents)

    # 마지막으로 변환한 stt 위치를 얻는 모듈
    info = dict(file_name=file_name, my_phone=my_phone,
                target_phone=target_phone)
    file_id, last_position = DbController.get_last_stt_position(info=info)

    if last_position < 0:
        return dict(success=False, msg="마지막 stt 위치를 가져오지 못함.")

    # 위에서 얻은 stt 위치로부터 음성 파일 끝까지 자르기
    crop_output_path = f"{temp_directory}/temp-{file_name}"
    FileController.crop_file(
        file_name=file_name, output_path=crop_output_path, start=last_position)

    ########## 여기에 AI 모듈 실행하고 score 산출 #############

    # crop 한 음성파일 stt 하고 DB 에 저장
    WhisperController.stt(last_position=last_position,
                          file_id=file_id, file_path=crop_output_path)

    # 최종 스코어
    score = random.randint(0, 100)

    ########## 끝 #############

    # score 가 50이 넘으면 보이스피싱 의심번호로 DB 에 저장
    if score >= 50:
        SpamManager.add_spam_phone(target_phone=target_phone)

    # (디버깅 출력용) file_id 와 일치하는 모든 stt 오름차순 출력
    DbController.print_all_stt(file_id=file_id)

    # 보이스피싱 결과 반환
    return dict(success=True, score=score)


# 전화가 오면 클라이언트에서 아래 api 를 요청, 보이스피싱 의심 번호인지 사전조회
@api_router.post("/check-phone/")
async def check_phone(target_phone: str):

    # 보이스피싱 번호이면 양수값 리턴, 아니면 0
    result = SpamManager.check_spam_phone(target_phone=target_phone)

    # 보이스피싱 번호이면
    if result >= 0:
        return dict(success=True, result=result)

    return dict(success=False, msg="보이스피싱번호 조회 실패")
