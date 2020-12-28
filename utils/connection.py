""" 데이터베이스 커낵션을 생성해 주는 파일

database 를 인자로 받아 connection 객체를 생성한뒤 반환해준다.

"""
import pymysql


def get_connection(database):
    connection = pymysql.connect(host=database['host'],
                                 user=database['user'],
                                 password=database['password'],
                                 db=database['name'],
                                 charset=database['charset'])
    return connection
