import os
import pickle
from util.file_util import FileUtil
from config import *
import sqlite3

class FileController:
    
    @staticmethod
    def save_pickle(file_name, file_contents):

        server_file_path = pick_directory + file_name

        # 해당 파일이 서버의 file 디렉토리에 이미 존재하면
        # if os.path.exists(server_file_path):
        #     데이터를 pickle 파일로 저장
        with open(server_file_path, 'wb') as file:
            pickle.dump(file_contents, file)
                    
    @staticmethod
    def get_pickle(file_name):
        
        server_file_path = pick_directory + file_name
        # 해당 파일이 서버의 file 디렉토리에 이미 존재하면
        if os.path.exists(server_file_path):
        # 저장된 데이터를 다시 읽어오기
            with open(server_file_path, 'rb') as file:
                return pickle.load(file)
        else:
            return [[], []]
        
    @staticmethod
    def save_file(file_name, file_contents):

        server_file_path = file_directory + file_name

        # 해당 파일이 서버의 file 디렉토리에 이미 존재하면
        if os.path.exists(server_file_path):

            copy_file_path = temp_directory + f"copy-{file_name}"
            temp_file_path = temp_directory + f"temp-{file_name}"

            FileUtil.write_file(copy_file_path, file_contents)
            FileUtil.append_wav(
                server_file_path, copy_file_path, temp_file_path)

            if os.path.exists(copy_file_path):
                os.remove(copy_file_path)

        # 최초 생성이면
        else:
            # 파일 생성 (클라이언트의 filename 그대로 사용)
            with open(server_file_path, "wb") as buffer:
                buffer.write(file_contents)

    @staticmethod
    def crop_file(file_name, output_path, start, end=None):

        server_file_path = file_directory + file_name

        FileUtil.crop_wav(input_path=server_file_path,
                          output_path=output_path, start=start, end=end)
