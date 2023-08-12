from mysql.manager.file_manager import FileManager


class DbController:

    # 마지막 stt 완료한 위치 가져옴
    @staticmethod
    def get_last_stt_position(info):

        # file 테이블에 file_name 이 있는지 확인, file_id 반환, 없으면 0 반환
        id = FileManager.get_file_id(info=info)

        if id < 1:  # 에러는 -1 리턴
            return id, -1

        return id, FileManager.get_max_end(file_id=id)  # 에러는 -1 리턴

    # file_id 의 모든 stt 레코드 print
    @staticmethod
    def print_all_stt(file_id):

        results = FileManager.read_all_stt(file_id=file_id)

        for row in results:
            print(row)
