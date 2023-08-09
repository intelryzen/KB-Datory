import pymysql
from config import *

MYSQL_HOST = 'localhost'
MYSQL_DB = 'KB_AI'

MYSQL_CONN = pymysql.connect(
    host=MYSQL_HOST,
    port=3306,
    user=MYSQL_CONFIG.USER,
    passwd=MYSQL_CONFIG.PW,
    db=MYSQL_DB,
    charset='utf8'
)

def conn_mysqldb():
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN


def initiate_db():
    db = conn_mysqldb()
    cursor = db.cursor()

    # spam_number 테이블 존재 체크 - > 없으면 생성
    table_name = 'spam_number'
    query = f"SHOW TABLES LIKE '{table_name}'"
    cursor.execute(query)
    exist_table = cursor.fetchone()
    if not exist_table:
        sql = f"""
        CREATE TABLE {table_name} (
            id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            phone CHAR(50),
            count INT DEFAULT 1,
            timestamp INT,
            PRIMARY KEY(id)
        );
        """
        cursor.execute(sql)
        db.commit()

    # file 테이블 존재 체크 - > 없으면 생성
    table_name = 'file'
    query = f"SHOW TABLES LIKE '{table_name}'"
    cursor.execute(query)
    exist_table = cursor.fetchone()
    if not exist_table:
        sql = f"""
        CREATE TABLE {table_name} (
            id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            file_name char(100),
            target_phone char(50),
            my_phone char(50),
            timestamp INT,
            PRIMARY KEY(id)
        );
        """
        cursor.execute(sql)
        db.commit()

    # stt 테이블 존재 체크 - > 없으면 생성
    table_name = 'stt'
    query = f"SHOW TABLES LIKE '{table_name}'"
    cursor.execute(query)
    exist_table = cursor.fetchone()
    if not exist_table:
        sql = f"""
        CREATE TABLE {table_name} (
            id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            file_id INT,
            start INT,
            end INT,
            speeker INT,
            text TEXT,
            PRIMARY KEY(id)
        );
        """
        cursor.execute(sql)
        db.commit()
