import traceback

import pymysql

from utils.custom_exceptions import DatabaseError, DataManipulationFail


class UserDao:
    """ Persistence Layer

        Attributes: None

        Author: 김민구

        History:
            2020-12-28(김민구): 초기 생성
            2020-12-31(김민구): 에러 문구 변경
    """

    def username_exist_check(self, connection, data):
        """ 유저 로그인아이디 중복 검사

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                0 : 해당 유저 없음
                1 : 해당 유저 존재

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-12-28(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
        """

        sql = """
            SELECT 
                EXISTS 
                    (SELECT id FROM accounts WHERE username = %(username)s) 
                AS user_exist;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchone()[0]
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def phone_exist_check(self, connection, data):
        """ 유저 전화번호 중복 검사

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                0 : 해당 유저 없음
                1 : 해당 유저 존재

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-12-28(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
        """

        sql = """
            SELECT 
                EXISTS 
                    (SELECT account_id FROM users WHERE phone = %(phone)s)
                AS user_exist;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchone()[0]
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def email_exist_check(self, connection, data):
        """ 유저 이메일 중복 검사

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                0 : 해당 유저 없음
                1 : 해당 유저 존재

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-12-28(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
        """

        sql = """
            SELECT 
                EXISTS 
                    (SELECT account_id FROM users WHERE email = %(email)s)
                AS user_exist;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchone()[0]
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def create_account(self, connection, data):
        """ account 생성

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                account_id : account 생성 후 아이디 반환

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러,
                500, {'message': 'data_manipulation_fail', 'error_message': '유저 등록을 실패하였습니다.'} : 데이터 조작 에러

            History:
                2020-12-28(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
                2021-01-02(김민구): 데이터 조작 에러 추가
        """

        sql = """
            INSERT INTO accounts (
                username 
                , password 
                , permission_type_id
            ) VALUES (
                %(username)s 
                , %(password)s 
                , %(permission_type_id)s
            );
        """

        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                if not result:
                    raise DataManipulationFail('유저 등록을 실패하였습니다.')
                return cursor.lastrowid

        except DataManipulationFail as e:
            raise e

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def create_user(self, connection, data):
        """ 유저 생성

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                0 : 유저 생성 실패
                1 : 유저 생성 성공

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러
                500, {'message': 'data_manipulation_fail', 'error_message': '유저 등록을 실패하였습니다.'} : 데이터 조작 에러

            History:
                2020-12-28(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
                2021-01-02(김민구): 데이터 조작 에러 추가
        """

        sql = """
            INSERT INTO users (
                account_id
                , phone
                , email
            ) VALUES (
                %(account_id)s 
                , %(phone)s
                , %(email)s
            );
        """

        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                if not result:
                    raise DataManipulationFail('유저 등록을 실패하였습니다.')

        except DataManipulationFail as e:
            raise e

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_user_infomation(self, connection, data):
        """ 유저 account_id, 로그인아이디, 비밀번호, permission_type 조회

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                {'account_id': 1, 'username': 'brandi', 'password': 'hashed_password', permission_type_id: 3}

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-12-29(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
        """

        sql = """
            SELECT 
                id
                , username 
                , password
                , permission_type_id
            FROM 
                accounts
            WHERE 
                username = %(username)s
                AND is_deleted=0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                return cursor.fetchone()

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def social_create_account(self, connection, data):
        """ 소셜 회원 account 생성

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                account_id : account 생성 후 아이디 반환

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'}  : 데이터베이스 에러
                500, {'message': 'data_manipulation_fail', 'error_message': '소셜 로그인을 실패하였습니다.'} : 데이터 조작 에러

            History:
                2020-12-29(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
                2021-01-02(김민구): 데이터 조작 에러 추가
        """

        sql = """
            INSERT INTO accounts (
                username 
                , permission_type_id
            ) VALUES (
                %(username)s 
                , %(permission_type_id)s
            );
        """

        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                if not result:
                    raise DataManipulationFail('소셜 로그인을 실패하였습니다.')

        except DataManipulationFail as e:
            raise e

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def social_create_user(self, connection, data):
        """ 소셜 회원 user 생성

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                0 : 유저 생성 실패
                1 : 유저 생성 성공

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'}  : 데이터베이스 에러
                500, {'message': 'data_manipulation_fail', 'error_message': '소셜 로그인을 실패하였습니다.'} : 데이터 조작 에러

            History:
                2020-12-29(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
                2021-01-02(김민구): 데이터 조작 에러 추가
        """

        sql = """
            INSERT INTO users (
                account_id
                , email
            ) VALUES (
                %(account_id)s 
                , %(email)s
            );
        """

        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                if not result:
                    raise DataManipulationFail('소셜 로그인을 실패하였습니다.')

        except DataManipulationFail as e:
            raise e

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')
