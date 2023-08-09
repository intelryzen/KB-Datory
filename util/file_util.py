import wave
import shutil
import os


class FileUtil:

    # temp 파일을 기존 (file 디렉토리) 음성 파일에 append 함.
    # file_path1 은 기존(원본) 파일, file_path2 는 append 할 파일, output_file_path 은 합쳐진 파일이 저장되는 경로로 원본 파일에 복제 후 사라짐(즉 temp 파일).
    @staticmethod
    def append_wavs(file_path1, file_path2, temp_file_path):
        # 파일들을 읽기 모드로 열기
        with wave.open(file_path1, 'rb') as w1, wave.open(file_path2, 'rb') as w2:
            # 파라미터 확인
            if w1.getnchannels() != w2.getnchannels() or w1.getsampwidth() != w2.getsampwidth() or w1.getframerate() != w2.getframerate():
                raise ValueError("WAV files have different parameters")

            # 새 파일을 쓰기 모드로 열기
            with wave.open(temp_file_path, 'wb') as output:
                output.setnchannels(w1.getnchannels())
                output.setsampwidth(w1.getsampwidth())
                output.setframerate(w1.getframerate())
                output.writeframes(w1.readframes(w1.getnframes()))
                output.writeframes(w2.readframes(w2.getnframes()))

        # 원본 파일에 복사
        shutil.move(temp_file_path, file_path1)

        # 필요 없는 파일 삭제
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if os.path.exists(file_path2):
            os.remove(file_path2)

    @staticmethod
    def write_file(file_path, contents):
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
