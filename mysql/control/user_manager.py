from mysql.mysql import conn_mysqldb

class UserManager:

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
