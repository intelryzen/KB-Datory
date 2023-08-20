import os
from fastapi import FastAPI
from api.api import api_router
from config import *
import sqlite3

# 현재 경로에 file 디렉토리 생성 (여기에 사용자의 음성 파일이 저장됨)
if not os.path.exists(file_directory):
    os.mkdir(file_directory)

# 현재 경로에 temp 디렉토리 생성 (여기에 temp 음성 파일이 저장됨)
if not os.path.exists(temp_directory):
    os.mkdir(temp_directory)

# emb 리스트 저장을 위한 pick 디렉토리 생성
if not os.path.exists(pick_directory):
    os.mkdir(pick_directory)

app = FastAPI()

@app.get("/")
async def home():
    return {"success": True}

app.include_router(
    api_router,
)

@app.on_event('startup')
async def startup():
    # 데이터베이스에 연결 (파일이 없으면 새로 생성됨)
    conn = sqlite3.connect('KB_AI.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS spam_number (id integer primary key, phone text, count integer DEFAULT 1, timestamp integer)''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS file (
        id INTEGER PRIMARY KEY,
        file_name TEXT,
        target_phone TEXT,
        my_phone TEXT,
        timestamp INTEGER
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stt (
        id INTEGER PRIMARY KEY,
        file_id INTEGER,
        start INTEGER,
        end INTEGER,
        speaker INTEGER,
        text TEXT
    );
    ''')
    conn.commit()
    conn.close()
    

# # 데이터 삽입
# cursor.execute("INSERT INTO stocks VALUES ('2021-08-19', 'BUY', 'AAPL', 100, 52.14)")

# # 변경사항 커밋

# # 데이터 조회
# for row in cursor.execute("SELECT * FROM stocks WHERE symbol='AAPL'"):
#     print(row)

# # 연결 종료
# conn.close()