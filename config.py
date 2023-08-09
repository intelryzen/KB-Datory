from private import Private

'''
private.py 파일 생성 필요

private.py:

    class Private:
        MYSQL_USER = "your_name"
        MYSQL_PW = "your_password"
    
'''

file_directory = 'file/'
temp_directory = 'temp/'

class MYSQL_CONFIG:
    USER = Private.MYSQL_USER
    PW = Private.MYSQL_PW
