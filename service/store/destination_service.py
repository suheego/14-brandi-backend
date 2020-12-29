from utils.custom_exceptions import DataLimitExceeded, NotUser

class DestinationService:

    def __init__(self, destination_dao):
        self.destination_dao = destination_dao

    def get_destination_detail_by_user_service(self, connection, data):
        """ 유저 배송지 조회 서비스

        View 에서 받은 connection 객체와 data를 model 계층으로 넘겨준다.

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 data 객체

        Author: 김기용

        Returns: 유저의 배송지 정보들 최대 5개

        Raises: 
            400, {'message': 'key_error', 'errorMessage': 'key_error'}  : 키값 불일치
            400, {'message': 'not_a_user', 'errorMessage': 'not_a_user'}: 유저 불일치
    

        History:
            2020-12-29(김기용): 초기 생성
        """
        try:
            # 1. check_account_type 메서드를 통해 permission_type 을 가져온다.
            permission_type = self.destination_dao.check_account_type(connection, data['account_id'])

            # permission_type 이 3이 아닐경우 예외발생(user == 3)
            if not permission_type == 3:
                raise NotUser('not_a_user')

            return self.destination_dao.get_user_destination(connection, data['account_id'])

        except KeyError:
            raise KeyError('key_error')

    def get_destination_detail_service(self, connection, data):
        """ 배송지 상세 정보 서비스

        View 에서 받은 connection 객체와 data를 model 계층으로 넘겨준다.

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 data 객체

        Author: 김기용

        Returns: 배송지 상세정보

        Raises: None

        History:
            2020-12-29(김기용): 초기 생성
        """
        return self.destination_dao.get_detail_destination(connection, data)

    def create_destination_service(self, connection, data):
        """ 배송지 생성 함수

        입력받은 account_id 의 permission_type 을 보고
        master, seller, user 인지 판단후 배송지 생성 여부를 결정한다.
        기본 배송지 값은 데이터베이스를 조회해서 없으면 설정해주고 있으면,
        0 값을 집어 넣어 준다.

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 김기용

        Returns: None

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값
            400, {'message':'destination_creation_denied', 'errorMessage':'not_a_user'}: 유저 불일치

        History:
            2020-12-28(김기용): 초기 생성
        """
        try:
            # 1. check_account_type 메서드를 통해 permission_type 을 가져온다.
            permission_type = self.destination_dao.check_account_type(connection, data['user_id'])

            # permission_type 이 3이 아닐경우 예외발생(user == 3)
            if not permission_type == 3:
                raise NotUser('not_a_user')

            # 2. check_default_location 함수를 사용해 해당 유저의
            #    모든 기본배송지 존재 여부를 true, false 로 반환 받는다.
            default_location_flag = self.destination_dao.check_default_location(connection, data['user_id'])

            # 3. 먼저 반환 데이터가 비어있는지 체크한다 = 비어 있을 경우 생성시 default_location을 1로 만들어준다.

            if default_location_flag:
                data['default_location'] = 0
            else:
                data['default_location'] = 1

            default_location_length_flag = self.destination_dao.check_default_location_length(connection, data['user_id'])

            if default_location_length_flag:
                raise DataLimitExceeded('max_destination_limit_reached')
            return self.destination_dao.create_destination_dao(connection, data)

        except KeyError:
            raise KeyError('key_error')

    def delete_destination_service(self, connection, data):
        try:
            # 1. check_account_type 메서드를 통해 permission_type 을 가져온다.
            permission_type = self.destination_dao.check_account_type(connection, data['user_id'])

            # permission_type 이 3이 아닐경우 예외발생(user == 3)
            if not permission_type == 3:
                raise NotUser('not_a_user')

            self.destination_dao.delete_destination_dao(connection, data)
        except KeyError:
            raise KeyError('key_error')
