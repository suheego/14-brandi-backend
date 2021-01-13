import pymysql

from utils.custom_exceptions import DeleteDenied, DestinationNotExist, DestinationCreateDenied, AccountNotExist, UpdateDenied


class DestinationDao:

    def update_default_location_true(self, connection, data):
        """기본 배송지가 없다면 기본배송지를 자동 설정해준다.

        Args:
            connection: 데이터베이스 연결 객체
            data: account_id 가 들어있다.
        Author: 김기용

        Returns: True/False

        Raises:
            400, {'message': 'unable_to_update', 'errorMessage': '기본 배송지 설정에 실패하였습니다.'}


        History:
            2020-12-30(김기용): 초기 생성
            2020-12-31(김기용): 수정실패시 예외처리 추가
            2020-01-02(김기용): 데코레이터 수정으로 인한 로직변경
        """

        sql = """
            UPDATE
                destinations
            SET
                default_location = 1
            WHERE
                user_id = %(account_id)s
                AND default_location = 0
                AND is_deleted = 0
                AND id <> %(destination_id)s
            LIMIT 1
            ;
        """

        with connection.cursor() as cursor:
            affected_row = cursor.execute(sql, data)
            if affected_row == 0:
                return UpdateDenied('기본 배송지 설정에 실패하였습니다.')

    def update_default_location_false(self, connection, data):
        """ 모든 기본 배송지의 정보를 False 로 만든다.

        Args:
            connection: 데이터베이스 연결 객체
            data      : service 에서 넘겨받은 data 객체

        Author: 김기용

        Returns: None

        Raises: 
            400, {'message': 'unable_to_update', 'errorMessage': '배송지 수정에 실패하였습니다.'}

        History:
            2020-12-30(김기용): 초기 생성
            2020-12-31(김기용): 리턴값 통일 
            2020-01-02(김기용): 데코레이터 수정으로 인한 로직
        """

        sql = """
        UPDATE
            destinations
        SET
            default_location = 0
        WHERE
            user_id = %(account_id)s
            AND default_location = 1
            AND is_deleted = 0
            ;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            affected_row = cursor.fetchone()
            if affected_row == 0:
                raise UpdateDenied('배송지 수정에 실패하였습니다.')

    def get_user_destination(self, connection, data):
        """ 해당 유저 배송지 조회

        데이터베이스에 해당 유저 배송지들을 검색한후 반환한다.

        Args:
            connection: 데이터베이스 연결 객체
            data      : service 에서 넘겨받은 data 객체

        Author: 김기용

        Returns: 해당 유저 배송지 정보들

        Raises: 
            400, {'message': 'destination_dose_not_exist', 'errorMessage': '배송지 정보가 존재하지 않습니다.'}

        History:
            2020-12-29(김기용): 초기 생성
            2020-01-02(김기용): is_deleted 가 추가되지 않아 논리삭제된 배송지정보도 조회가 가능했던 문제 수정
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
                user_id=%s
                AND is_deleted=0
                ;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            if not result:
                raise DestinationNotExist('배송지 정보가 존재하지 않습니다.')
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
            400, {'message': 'destination_dose_not_exist', 'errorMessage': '배송지 정보가 존재하지 않습니다.'}

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
                id=%s
                AND is_deleted = 0
                ;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data['destination_id'])
            result = cursor.fetchall()
            if not result:
                raise DestinationNotExist('배송지 정보가 존재하지 않습니다.')
            return result

    def create_destination_dao(self, connection, data):
        """  배송지 생성

        Args:
            connection: 데이터베이스 연결 객체
            data      : 배송지 정보가 담겨있는 객체

        Author: 김기용

        Returns: None

        Raises:
            400, {'message': 'unable_to_create', 'errorMessage': '배송지 생성에 실패하였습니다.'}

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
        )
        ;
        """
        with connection.cursor() as cursor:
            affected_row = cursor.execute(sql, data)
            if affected_row == 0:
                raise DestinationCreateDenied('배송지 생성에 실패하였습니다.')


    def check_default_location(self, connection, data):
        """ 배송지 아이디로 기본 배송지인지 조회

        삭제 이후의 DB 에 남아 있는 배송지 정보 들중에
        기본 배송지 정보를 가진 배송지가 있는지 조회한다.
        COUNT 로 존재 유무를 파악한다. 기본 배송지가
        있을 경우 1을 반환 하고 없을 경우 0 을 반환 한다.

        Args:
            connection : 데이터베이스 연결 객체
            data       : user_id, 와 account_id 를 담고 있는 객체

        Author: 김기용

        Returns: 0, 1

        Raises: None

        History:
            2020-12-28(김기용): 초기 생성
            2020-12-30(김기용): 한개만 조회하기때문에 fetchone 을 적용
        """
        sql = """
        SELECT COUNT(*) 
        FROM
            destinations 
        WHERE
            user_id = %(account_id)s
        AND is_deleted=0 
        AND default_location=1
        ;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            default_location = cursor.fetchone()

            # 튜플 형식으로 반환되기 때문에 인덱스로 접근해서 숫자값만 반환해준다.
            return default_location[0]

    def check_default_location_by_user(self, connection, account_id):
        """ 유저 아이디로 배송지를 가지고 있는지 조사

        account_id 에 해당하는 유저의 모든 배송지 기본 값을
        조회해서 반환한다.

        Args:
            connection: 데이터베이스 연결 객체
            account_id: 계정 아이디

        Author: 김기용

        Returns: None, (1, 0)

        Raises: None

        History:
            2020-12-28(김기용): 초기 생성
            2021-01-02(김기용): 논리삭제 여부 조건 추가.
        """

        sql = """
        SELECT
            default_location
        FROM
            destinations
        WHERE
            user_id=%s
        AND default_location = 1
        AND is_deleted = 0
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, account_id)
            default_location = cursor.fetchone()

            # 튜플 형식을 반환해준다: 기본배송지가 존재하지 않을경우 None 을 반환한다.
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

        Raises: {'message':'invalid_delete_command_access', 'errorMessage':'배송지 삭제에 실패했습니다.'}

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
        AND user_id=%(account_id)s
        AND is_deleted=0
        ;
        """

        with connection.cursor() as cursor:
            affected_row = cursor.execute(sql, data)
            if affected_row == 0:
                raise DeleteDenied('배송지 삭제에 실패했습니다.')

    def update_destination_info_dao(self, connection, data):
        """ 유저의 배송지 정보 수정

            배송지의 정보를 수정한다, 만약 기본배송지가 수정이된다면
            입력되는 값을 제외한 데이터 중에서 기본 배송지 유무를 판단하여
            default_location 값을 바꿔준다.

        Args:
            connection: 데이터베이스 연결 객체
            data      : destination_id, account_id 가 담겨있는 객체

        Author: 김기용

        Returns: int 형 정수

        Raises: {'message':'unable_to_update', 'errorMessage':'배송지를 수정할수 없습니다.'}

        History:
            2020-12-29(김기용): 초기 생성
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
                raise UpdateDenied('배송지를 수정할수 없습니다.')


    def check_default_flag(self, connection, data):
        """ 배송지 아이디로 기본 배송지인지 조회

            변경하려는 배송지 정보가 기본 배송지인지 조회한다.

        Args:
            connection : 데이터베이스 연결 객체
            data       : user_id, 와 account_id 를 담고 있는 객체

        Author: 김기용

        Returns: True, False

        Raises: None

        History:
            2020-12-28(김기용): 초기 생성
            2020-12-30(김기용): 한개만 조회하기때문에 fetchone 을 적용
        """
        sql = """
        SELECT 
            id
        FROM
            destinations 
        WHERE
            user_id = %(account_id)s
            AND id = %(destination_id)s
            AND default_location = 1
            AND is_deleted=0 
            ;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            flag = cursor.fetchone()
            return flag
