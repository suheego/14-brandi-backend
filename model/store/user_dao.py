import pymysql

from utils.custom_exceptions import DatabaseError, UserCreateDenied


class UserDao:
    """ Persistence Layer

        Attributes: None

        Author: 김민구

        History:
            2020-20-28(김민구): 초기 생성
    """

    def username_exist_check(self, connection, data):
        """ 유저 로그인아이디 중복 검사

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                return 0 : 해당 유저 없음
                return 1 : 해당 유저 존재

            Raises:
                500, {'message': 'database_error', 'errorMessage': 'database_error_' + format(e)}: 데이터베이스 에러

            History:
                2020-20-28(김민구): 초기 생성
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

        except Exception as e:
            raise DatabaseError('database_error_' + format(e))

    def phone_exist_check(self, connection, data):
        """ 유저 전화번호 중복 검사

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                return 0 : 해당 유저 없음
                return 1 : 해당 유저 존재

            Raises:
                500, {'message': 'database_error', 'errorMessage': 'database_error_' + format(e)}: 데이터베이스 에러

            History:
                2020-20-28(김민구): 초기 생성
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

        except Exception as e:
            raise DatabaseError('database_error_' + format(e))

    def email_exist_check(self, connection, data):
        """ 유저 이메일 중복 검사

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                return 0 : 해당 유저 없음
                return 1 : 해당 유저 존재

            Raises:
                500, {'message': 'database_error', 'errorMessage': 'database_error_' + format(e)}: 데이터베이스 에러

            History:
                2020-20-28(김민구): 초기 생성
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

        except Exception as e:
            raise DatabaseError('database_error_' + format(e))

    def create_account(self, connection, data):
        """ account 생성

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                return account_id : account 생성 후 아이디 반환

            Raises:
                500, {'message': 'database_error', 'errorMessage': 'database_error_' + format(e)}: 데이터베이스 에러

            History:
                2020-20-28(김민구): 초기 생성
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
                cursor.execute(sql, data)
                return cursor.lastrowid

        except Exception as e:
            raise DatabaseError('database_error_' + format(e))

    def create_user(self, connection, data):
        """ 유저 생성

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                None

            Raises:
                500, {'message': 'user_create_denied', 'errorMessage': 'user_create_fail'}       : 유저 생성 실패
                500, {'message': 'database_error', 'errorMessage': 'database_error_' + format(e)}: 데이터베이스 에러

            History:
                2020-20-28(김민구): 초기 생성
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
                    raise UserCreateDenied('user_create_fail')

        except Exception as e:
            raise DatabaseError('database_error_' + format(e))

    def get_username_password(self, connection, data):
        """ 유저 로그인아이디, 비밀번호 조회

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                {'account_id' : 1, 'username': 'kimminkoo', 'password' : 'hashed_password'}

            Raises:
                500, {'message': 'database_error', 'errorMessage': 'database_error_' + format(e)}: 데이터베이스 에러

            History:
                2020-20-29(김민구): 초기 생성
        """

        sql = """
            SELECT 
                id
                , username
                , password
            FROM 
                accounts 
            WHERE 
                username = %(username)s;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                return cursor.fetchone()

        except Exception as e:
            raise DatabaseError('database_error_' + format(e))