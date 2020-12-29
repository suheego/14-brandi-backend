import pymysql

from utils.custom_exceptions import DestinationNotExist, DestinationCreateDenied, AccountNotExist, DataLimitExceeded


class DestinationDao:

    def get_user_destination(self, connection, data):
        """ 해당 유저 배송지 조회

        데이터베이스에 해당 유저 배송지들을 검색한후 반환한다.

        Args:
            connection: 데이터베이스 연결 객체
            data      : service 에서 넘겨받은 data 객체

        Author: 김기용

        Returns: 해당 유저 배송지 정보들

        Raises: 
            400, {'message': 'destination_dose_not_exist', 'errorMessage': 'destination_dose_not_exist'}: 배송지 조회 실패

        History:
            2020-12-29(김기용): 초기 생성
        """
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
                user_id=%s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            if not result:
                raise DestinationNotExist('destination_does_not_exist')
            return result

    def get_detail_destination(self, connection, data):
        """ 배송지 상세 정보 조회

        데이터베이스에 destination_id 를 가지고 데이터를 조회한다.

        Args:
            connection: 데이터베이스 연결 객체
            data      : service 에서 넘겨받은 data 객체

        Author: 김기용

        Returns: 배송지 상세 정보

        Raises: 
            400, {'message': 'destination_dose_not_exist', 'errorMessage': 'destination_dose_not_exist'}: 배송지 조회 실패

        History:
            2020-12-29(김기용): 초기 생성
        """
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
                id=%s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data['destination_id'])
            result = cursor.fetchall()
            if not result:
                raise DestinationNotExist('destination_does_not_exist')
            return result

    def create_destination_dao(self, connection, data):
        """  배송지 생성

        Args:
            connection: 데이터베이스 연결 객체
            data      : 배송지 정보가 담겨있는 객체

        Author: 김기용

        Returns: None

        Raises:
            400, {'message': 'unable_to_create', 'errorMessage': 'unable_to_create'}: 계정 생성 실패

        History:
            2020-12-28(김기용): 초기 생성
        """

        sql = """
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
        """ 기본 배송지 값 조회

        account_id 에 해당하는 유저의 모든 배송지 기본 값을
        조회해서 반환한다.

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
        sql = """
        SELECT
            default_location
        FROM
            destinations
        WHERE
            user_id=%s
        AND
            default_location = 1;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, account_id)
            default_location = cursor.fetchall()

            print('check_default_location:', bool(default_location))
            return default_location

    def check_default_location_length(self, connection, account_id):

        sql = """
        SELECT COUNT(*) as cnt
        FROM
            destinations
        WHERE
            user_id = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, account_id)
            counts = cursor.fetchone()

            print('check_default_location_lenth:', counts)
            return counts
            
    def delete_destination_dao(self, connection, data):

        sql = """
        UPDATE
            is_deleted
        FROM
            destinations
        WHERE
            id=%(destination_id)s
        AND
            user_id=%(user_id)s;
        """

        with connection.cursor() as cursor:
            affected_row = cursor.execute(sql, data)
            if affected_row == 0:
                raise DeleteFailed('unable_to_delete_destinations')
