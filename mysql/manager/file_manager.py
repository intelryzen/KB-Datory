from datetime import datetime
from mysql.mysql import conn_mysqldb


class FileManager:

    # file 테이블에서 file_name 찾아서 id 값 반환
    @staticmethod
    def get_file_id(info):

        try:
            db = conn_mysqldb()

            with db.cursor() as cursor:
                sql = "SELECT id FROM file WHERE file_name = %s"
                cursor.execute(sql, (info["file_name"]))

                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return FileManager.create_file(info)
        except:
            return 0

        # finally:
        #     db.close()

    # file 레코드 생성
    @staticmethod
    def create_file(info):

        try:
            db = conn_mysqldb()

            with db.cursor() as cursor:
                sql = """
                INSERT INTO file (file_name, target_phone, my_phone, timestamp)
                VALUES (%s, %s, %s, %s)
                """
                timestamp = int(datetime.now().timestamp())
                cursor.execute(
                    sql, (info["file_name"], info["target_phone"], info["my_phone"], timestamp))

            db.commit()

            with db.cursor() as cursor:
                cursor.execute("SELECT LAST_INSERT_ID()")
                result = cursor.fetchone()

                if result:
                    return result[0]
                else:
                    return 0
        # except:
        #     return 0

        finally:
            db.close()

    # stt 에서 file_id 와 일치한 레코드 중 가장 큰 end 값 반환
    @staticmethod
    def get_max_end(file_id):

        try:
            db = conn_mysqldb()

            with db.cursor() as cursor:
                sql = """
                SELECT MAX(end) FROM stt
                WHERE file_id = %s
                """
                cursor.execute(sql, (file_id,))

                result = cursor.fetchone()
                if result[0]:
                    return result[0]
                else:
                    return 0
        except:
            return -1

        # finally:
        #     db.close()

    # stt 테이블에 insert
    @staticmethod
    def insert_stt(file_id, data):
        try:
            db = conn_mysqldb()

            with db.cursor() as cursor:
                sql = """
                INSERT INTO stt (file_id, start, end, speeker, text)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(
                    sql, (file_id, data['start'], data['end'], data['speaker'], data['text']))

            db.commit()
        except:
            pass
        # finally:
        #     db.close()

    # stt 테이블에 모든 file_id 레코드를 end 오름차순 가져오기
    def read_all_stt(file_id):

        try:
            db = conn_mysqldb()

            with db.cursor() as cursor:
                sql = """
                SELECT * FROM stt
                WHERE file_id = %s
                ORDER BY end ASC
                """
                cursor.execute(sql, (file_id,))

                results = cursor.fetchall()

                return results
        except:
            return []

        # finally:
        #     db.close()

    # def create_user_table(table_name: str):
    #     db = conn_mysqldb()
    #     cursor = db.cursor()

    #     query = f"SHOW TABLES LIKE '{table_name}'"
    #     cursor.execute(query)
    #     exist_table = cursor.fetchone()

    #     if not exist_table:
    #         sql = f"""
    #         CREATE TABLE {table_name} (
    #             id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    #             phone CHAR(50),
    #             count INT DEFAULT 1,
    #             timestamp INT,
    #             PRIMARY KEY(id)
    #         );
    #         """
    #         cursor.execute(sql)
    #         db.commit()
