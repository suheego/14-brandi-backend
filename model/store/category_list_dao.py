import traceback

import pymysql

from utils.custom_exceptions import DatabaseError


class CategoryListDao:
    def get_first_category_list(self, connection):
        """ menu 카테고리 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                result (menus)

            Raises:
                500, {'message': 'database_error', 'errorMessage': format(e)} : 데이터베이스 에러

            History:
                2020-12-30(김민구): 초기 생성
        """

        sql = """
            SELECT 
                id
                , `name`
            FROM 
                menus
            WHERE
                is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_second_category_list(self, connection):
        """ main 카테고리 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                result (main_categories)

            Raises:
                500, {'message': 'database_error', 'errorMessage': format(e)} : 데이터베이스 에러

            History:
                2020-12-30(김민구): 초기 생성
        """

        sql = """
            SELECT 
                id 
                , `name`
                , menu_id 
            FROM 
                main_categories
            WHERE     
                is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_third_category_list(self, connection):
        """ sub 카테고리 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                result (sub_categories)

            Raises:
                500, {'message': 'database_error', 'errorMessage': format(e)} : 데이터베이스 에러

            History:
                2020-12-30(김민구): 초기 생성
        """

        sql = """
            SELECT 
                id
                , `name`
                , main_category_id 
            FROM 
                sub_categories
            WHERE
                is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')
