from utils.custom_exceptions import DataLimitExceeded, NotUser


class DestinationService:

    def __init__(self, destination_dao):
        self.destination_dao = destination_dao
# 여기서 dao 를 넣었다면..... 중앙관리 장점 단점 생각해보자..

    def update_destination_info_service(self, connection, data):
        """ 유저 배송지 정보 수정

            1. data 로 건네받은  기본 배송지(default_location = 1) 값이 존재하는지 True / false
            2. 기본 배송지는 오직 1개만 존재할 수 있기때문에 True 일 경우 기본 배송지 변경
            3. 수정 진행
        """
        try:
            # 1
            if data['default_location'] == "1":
                default_location_flag = True
            else:
                default_location_flag = False
            if default_location_flag:
                # 2
                self.destination_dao.make_default_location_false(connection, data)
            # 3
            return self.destination_dao.update_destination_info_dao(connection, data)

        except KeyError:
            raise KeyError('key_error')

    def get_destination_detail_by_user_service(self, connection, data):
        """ 유저 배송지 조회 서비스

        1. permission_type 을 통해 user 가 맞는지 확인한다
        2. 유저가 아닐경우 예외처리
        3. 유저 정보 조회

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
            # 1
            permission_type = self.destination_dao.check_account_type(connection, data['account_id'])

            # 2
            if not permission_type == 3:
                raise NotUser('not_a_user')
            
            # 3
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

        1. 유저인지 확인 True/False
        2. 해당 유저의 배송지 정보가 5개를 초과하는지 체크 True/False
        3. 없으면 default_location 설정 
        4. 유저 생성


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
            2020-12-29(김기용): [리뷰반영] 로직 간단하게 수정

        """
        try:
            # 1.
            permission_type = self.destination_dao.check_account_type(connection, data['user_id'])
            if not permission_type == 3:
                raise NotUser('not_a_user')

            # 2.
            default_location_length_flag = self.destination_dao.check_default_location_length(connection, data['user_id'])
            if default_location_length_flag >= 5:
                raise DataLimitExceeded('max_destination_limit_reached')

            # 3
            default_location_flag = self.destination_dao.check_default_location_by_user(connection, data['user_id'])
            if not default_location_flag:
                data['default_location'] = 1
            else:
                data['default_location'] = 0

            # 4
            return self.destination_dao.create_destination_dao(connection, data)

        except KeyError:
            raise KeyError('key_error')

    def delete_destination_service(self, connection, data):
        """ 배송지 삭제 서비스

        1. 계정이 유저인지 확인 True/False
        2. 삭제
        3. 기본 배송지 값이 지워졌을 수도 있으므로 기본값이 있는지 확인 True/False
        4. 기본 배송지가 삭제 되었다면 기본 배송지 자동 설정  

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 김기용

        Returns: None

        Raises:
            400, {'message': 'not_a_user', 'errorMessage': 'not_a_user'}: 유저 불일치
            400, {'message':'key_error', 'errorMessage':'key_error'}: 잘못 입력된 키값

        History:
            2020-12-29(김기용): 초기 생성 및 [리뷰반영] COUNT 와 LIMIT 사용해서 로직 구현해보기
            2020-12-30(김기용): 1, 2, 3, 4로직 구현

        """
        try:
            # 1
            permission_type = self.destination_dao.check_account_type(connection, data['account_id'])
            if not permission_type == 3:
                raise NotUser('not_a_user')

            # 2
            self.destination_dao.delete_destination_dao(connection, data)

            # 3
            default_location_flag = self.destination_dao.check_default_location(connection, data)

            # 4
            if not default_location_flag:
                self. destination_dao.update_default_location(connection, data)

            return 0

        except KeyError:
            raise KeyError('key_error')
