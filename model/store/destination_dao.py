import pymysql

from utils.custom_exceptions import DestinationNotExist, DestinationCreateDenied, AccountNotExist, DataLimitExceeded


class DestinationSelectDao:

    def select_destination(self, connection, data):

        sql = """
            SELECT
                id
                , user_id
                , recipient
                , phone
                , address1
                , address2
                , post_number
                , default_location
            FROM
                destinations
            WHERE
                id = %(destination_id)s;
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            if not result:
                raise DestinationNotExist('destination_does_not_exist')
            return result

    def create_destination_dao(self, connection, data):

        sql ="""
        INSERT INTO destinations (
            user_id
            , recipient
            , phone
            , address1
            , address2
            , post_number
            , default_location
        ) VALUES (
            %(user_id)s
            , %(recipient)s
            , %(phone)s
            , %(address1)s
            , %(address2)s
            , %(post_number)s
            , %(default_location)s
        );
        """
        with connection.cursor() as cursor:
            affected_row = cursor.execute(sql, data)
            if affected_row == 0:
                raise DestinationCreateDenied('unable_to_create')

    def check_account_type(self, connection, account_id):
        """ 계정 종류 확인 함수

        account_id 값으로 계정 종류를 확인한다.
        master(1), seller(2), user(3)


        Args:
            connection: 데이터베이스 연결 객체
            account_id: 계정 아이디

        Author: 김기용

        Returns: 3: user

        Raises:
            400, {'message': 'account_does_not_exist', 'errorMessage': 'account_does_not_exist}: 계정 정보 없음

        History:
            2020-12-28(김기용): 초기 생성
        """
        sql ="""
        SELECT
            permission_type_id
        FROM
            accounts
        WHERE
            id=%s;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, account_id)
            permission_type_id = cursor.fetchall()
            if not permission_type_id:
                raise AccountNotExist('account_does_not_exist')
            return permission_type_id[0][0]

    def check_default_location(self, connection, account_id):
        """ 계정 종류 확인 함수

        account_id 값으로 계정 종류를 확인한다.
        master(1), seller(2), user(3)


        Args:
            connection: 데이터베이스 연결 객체
            account_id: 계정 아이디

        Author: 김기용

        Returns: 3: user

        Raises:
            400, {'message': 'account_does_not_exist', 'errorMessage': 'account_does_not_exist'}: 계정 정보 없음
            400, {'message': 'data_limit_reached', 'errorMessage': 'max_destination_limit_reached'}: 계정 정보 없음

        History:
            2020-12-28(김기용): 초기 생성
        """
        sql ="""
        SELECT
            default_location
        FROM
            destinations
        WHERE
            user_id=%s;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, account_id)
            default_location = cursor.fetchall()

            # 배송지 5개가 넘어가면 예외처리
            if len(default_location) >= 5:
                raise DataLimitExceeded('max_destination_limit_reached')
            return default_location
