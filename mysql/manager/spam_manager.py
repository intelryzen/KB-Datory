from datetime import datetime
from mysql.mysql import conn_mysqldb


class SpamManager:

    # spam 테이블에서 보이스피싱의심번호 추가
    @staticmethod
    def add_spam_phone(target_phone):

        try:
            db = conn_mysqldb()

            with db.cursor() as cursor:

                check_sql = "SELECT * FROM spam_number WHERE phone = %s LIMIT 1"

                cursor.execute(check_sql, (target_phone,))

                # db 에 없으면
                if cursor.fetchone() is None:

                    sql = """
                    INSERT INTO spam_number (phone, count, timestamp)
                    VALUES (%s, %s, %s)
                    """

                    timestamp = int(datetime.now().timestamp())
                    count = 1

                    cursor.execute(sql, (target_phone, count, timestamp))

                db.commit()
        except:
            pass
        # finally:
        #     db.close()

    # spam 테이블에서 보이스피싱의심번호인지 조회, 맞다면 count(<- 보이스피싱범이 전화건 횟수) 1 증가하고 count 반환

    @staticmethod
    def check_spam_phone(target_phone):

        try:
            db = conn_mysqldb()

            with db.cursor() as cursor:

                check_sql = "SELECT count FROM spam_number WHERE phone = %s LIMIT 1"
                cursor.execute(check_sql, (target_phone,))
                result = cursor.fetchone()

                if result:
                    update_sql = "UPDATE spam_number SET count = count + 1 WHERE phone = %s"
                    cursor.execute(update_sql, (target_phone,))
                    db.commit()

                    return result[0] + 1  # count 반환
                else:
                    return 0
        except:
            return -1
        # finally:
        #     db.close()
