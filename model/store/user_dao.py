import pymysql

from utils.custom_exceptions import DatabaseError


class UserDao:
    """ Persistence Layer

            Attributes: None

            Author: 김민구

            History:
                2020-20-28(김민구): 초기 생성
        """

    def user_exist_check(self, connection, data):
        sql = """
        SELECT
	        EXISTS 
		        (SELECT account_id FROM users WHERE email = %(email)s) OR
	        EXISTS 
		        (SELECT account_id FROM users WHERE phone = %(phone)s) OR
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
            raise DatabaseError('database error ' + format(e))

    def create_account(self, connection, data):
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
            raise DatabaseError('database error ' + format(e))

    def create_user(self, connection, data):
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
                cursor.execute(sql, data)

        except Exception as e:
            raise DatabaseError('database error ' + format(e))
