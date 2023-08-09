import os
from fastapi import FastAPI
from api.api import api_router
from config import *

# 현재 경로에 file 디렉토리 생성 (여기에 사용자의 음성 파일이 저장됨)
if not os.path.exists(file_directory):
    os.mkdir(file_directory)

# 현재 경로에 temp 디렉토리 생성 (여기에 temp 음성 파일이 저장됨)
if not os.path.exists(temp_directory):
    os.mkdir(temp_directory)

app = FastAPI()

app.include_router(
    api_router,
)
