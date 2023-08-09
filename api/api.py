import random
from fastapi import APIRouter
from fastapi import File, UploadFile
from control.file_control import FileController
from control.whisper_control import WhisperController

api_router = APIRouter(
    prefix="/api",
    tags=["API"],
)


@api_router.post("/score/")
async def get_score(file: UploadFile = File(...)):

    # 클라이언트로부터 받아온 wav (15 초) 파일
    file_name = file.filename
    file_contents = await file.read()

    # 서버에 파일을 저장하는 모듈
    FileController.save_file(file_name, file_contents)
    # FileController.crop_file("test.wav")

    # AI 모듈
    WhisperController.stt("file/" + file_name)

    # 보이스피싱 결과 반환
    return {"score": random.randint(0, 100)}
