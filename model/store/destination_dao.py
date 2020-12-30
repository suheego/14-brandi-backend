import pymysql

from utils.custom_exceptions import DeleteDenied, DestinationNotExist, DestinationCreateDenied, AccountNotExist, UpdateDenied


class DestinationDao:

    def make_default_location_false(self, connection, data):
        """ 기본 배송지의 정보를 False 로 만든다.

        Args:
            connection: 데이터베이스 연결 객체
            data      : service 에서 넘겨받은 data 객체

        Author: 김기용

        Returns: None

        Raises: 
            400, {'message': 'unable_to_update', 'errorMessage': 'unable_to_update_destination'}: 배송지 수정 실패

        History:
            2020-12-30(김기용): 초기 생성
        """

        sql = """
        UPDATE
            destinations
        SET
            default_location = 0
        WHERE
            user_id = %(account_id)s
            AND default_location = 1
            AND is_deleted = 0;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            # fetchone()
            affected_row = cursor.fetchall()
            if affected_row == 0:
                raise UpdateDenied('unable_to_delete_destinations')
            #리턴값 통일.
            # return 할 필요가 없다.. 예외처리를 일관성 있게 처리하는 방법을 생각해보자.
            return affected_row

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

    def check_account_type(self, connection, account_id): #유저에 대한 내용이기때문에 user 에서처리
        """ 계정 종류 확인 함수
            서비스가 여러개의 DAO를 가지는게 어렵지 않지만,

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

    def update_default_location(self, connection, data):
        """기본 배송지가 삭제 되었다면 기본배송지를 자동 설정해준다.

        Args:
            connection: 데이터베이스 연결 객체
            account_id: 계정 아이디

        Author: 김기용

        Returns: True/False

        Raises: None

        History:
            2020-12-30(김기용): 초기 생성
        """

        sql = """
            UPDATE
                destinations
            SET
                default_location = 1
            WHERE
                is_deleted = 0
            AND 넣자...
            ORDER BY
            
            
            LIMIT 1;
        """

        with connection.cursor() as cursor:
            return cursor.execute(sql, data)
            ### result = cursor.fetchall()
            ###return result

    def check_default_location(self, connection, data):
        """ 배송지 아이디로 기본 배송지인지 조회

        Args:
            connection : 데이터베이스 연결 객체
            data       : user_id, 와 account_id 를 담고 있는 객체

        Author: 김기용

        Returns: 3: True, False

        Raises:
            400, {'message': 'account_does_not_exist', 'errorMessage': 'account_does_not_exist'}: 계정 정보 없음
            400, {'message': 'data_limit_reached', 'errorMessage': 'max_destination_limit_reached'}: 계정 정보 없음

        History:
            2020-12-28(김기용): 초기 생성
        """
        sql = """
        SELECT COUNT(*) 
        FROM
            destinations 
        WHERE
            user_id = %(account_id)s
        AND is_deleted=0 
        AND default_location=1;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            # fetchone() 1개일 경우는 ,,
            default_location = cursor.fetchall()

            return default_location[0][0]

    def check_default_location_by_user(self, connection, account_id):
        """ 유저 아이디로 배송지를 가지고 있는지 조사

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
        AND default_location = 1
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, account_id)
            default_location = cursor.fetchall()

            return default_location

    def check_default_location_length(self, connection, account_id):
        """ 배송지 데이터 개수 반환

        데이터 배송지 데이터의 개수를 반환한다.

        Args:
            connection: 데이터베이스 연결 객체
            account_id: 계정 아이디

        Author: 김기용

        Returns: int 형 정수

        Raises: None

        History:
            2020-12-29(김기용): 초기 생성
            2020-12-30(김기용): [수정]쿼리문 조건 추가 is_deleted=0
        """

        sql = """
        SELECT COUNT(*)
        FROM
            destinations
        WHERE
            user_id = %s
            AND is_deleted = 0;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, account_id)
            counts = cursor.fetchone()

            return counts[0]
            
    def delete_destination_dao(self, connection, data):
        """ 배송지 논리 삭제

        배송지 is_delete 필드를 True 바꿔준다.

        Args:
            connection: 데이터베이스 연결 객체
            data      : destination_id, account_id 가 담겨있는 객체

        Author: 김기용

        Returns: int 형 정수

        Raises: {'message':'invalid_delete_command_access', 'errorMessage':'unable_to_delete_destinations'}

        History:
            2020-12-29(김기용): 초기 생성
        """

        sql = """
        UPDATE
            destinations
        SET
            is_deleted = 1
        WHERE
            id=%(destination_id)s
        AND user_id=%(account_id)s;
        """

        with connection.cursor() as cursor:
            affected_row = cursor.execute(sql, data)
            if affected_row == 0:
                raise DeleteDenied('unable_to_delete_destinations')

    def update_destination_info_dao(self, connection, data):
        """ 유저의 배송지 정보 수정

            작성중...
        """
        sql = """
        UPDATE 
            destinations
        SET
            recipient = %(recipient)s,
            phone = %(phone)s,
            address1 = %(address1)s,
            address2 = %(address2)s,
            post_number = %(post_number)s,
            default_location = %(default_location)s
        WHERE
            id = %(destination_id)s
        """
        with connection.cursor() as cursor:
            affected_row = cursor.execute(sql, data)
            if affected_row == 0:
                raise UpdateDenied('unable_to_update_destinations')
