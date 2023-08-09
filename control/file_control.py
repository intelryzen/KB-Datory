import os
from util.file_util import FileUtil
from config import *


class FileController:

    @staticmethod
    def saveFile(file_name, file_contents):

        server_file_path = file_directory + file_name

        # 해당 파일이 서버의 file 디렉토리에 이미 존재하면
        if os.path.exists(server_file_path):

            copy_file_path = temp_directory + f"copy-{file_name}"
            temp_file_path = temp_directory + f"temp-{file_name}"

            FileUtil.write_file(copy_file_path, file_contents)
            FileUtil.append_wavs(
                server_file_path, copy_file_path, temp_file_path)

        # 최초 생성이면
        else:

            # 파일 생성 (클라이언트의 filename 그대로 사용)
            with open(server_file_path, "wb") as buffer:
                buffer.write(file_contents)
