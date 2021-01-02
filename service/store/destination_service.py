from utils.custom_exceptions import DataLimitExceeded, NotUser


class DestinationService:

    def __init__(self, destination_dao):
        self.destination_dao = destination_dao

    def update_destination_info_service(self, connection, data):
        """ 유저 배송지 정보 수정
        
        기본 배송지설정 여부를 체크해서 데이터에 기본배송지 값이 하나도 존재하지 않는다면
        데이터중 하나를 기본배송지로 바꾸어준다.

        Args:
            connection: 데이터베이스 커넥션 객체
            data      : 수정할 배송지 데이터 정보

        Author: 김기용

        Returns:
            200, {'message': 'success', 'result': 상품정보들}   
        
        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            500, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러
        History:

                2020-12-30(김기용): 초기 생성
                2020-12-31(김기용): 1차 구현
                2021-01-01(김기용): 복잡한 로직을 간단하게 수정
                2021-01-02(김기용): decorator 변경으로 인한 로직 수정
        """
        try:
            if not data['permission_type_id'] == 3:
                raise NotUser('유저가 아닙니다.')
            # 들어오는  default_location 값에 따라 기본 배송지 여부를 결정해준다.
            if data['default_location'] == "1":
                self.destination_dao.update_default_location_false(connection, data)
            else:
                self.destination_dao.update_default_location_true(connection, data)

            # 3. 수정 진행
            return self.destination_dao.update_destination_info_dao(connection, data)

        except KeyError:
            raise KeyError('key_error')

    def get_destination_detail_by_user_service(self, connection, data):
        """ 유저 배송지 조회 서비스

        1. permission_type 을 통해 user 가 맞는지 확인한다
        2. 유저 정보 조회

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
            2020-12-30(김기용): 1차 구현
            2020-12-31(김기용): 복잡한 로직을 간단하게 수정.
            2021-01-02(김기용): 유저의 종류를 데코레이터에서 처리로 변경.
        """
        try:
            if not data['permission_type_id'] == 3:
                raise NotUser('유저가 아닙니다.')
            
            # 2. 유저 정보 조회
            return self.destination_dao.get_user_destination(connection, data['account_id'])

        except KeyError:
            raise KeyError('키 값이 일치하지 않습니다.')

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
            2020-12-30(김기용): 로직위에 간단한 설명 주석 삽입
            2020-12-31(김기용): DAO 부분에서 처리해주던 USER 검증 과정을 데코레이터 부분에서 처리하도록 수정, check_account_type_dao 삭제 

        """
        try:
            # 1. 유저인지 확인 True/False
            if not data['permission_type_id'] == 3:
                raise NotUser('not_a_user')

            # 2. 해당 유저의 배송지 정보가 5개를 초과하는지 체크 True/False
            default_location_length_flag = self.destination_dao.check_default_location_length(connection, data['user_id'])
            if default_location_length_flag >= 5:
                raise DataLimitExceeded('최대 입력할 수 있는 배송지 개수를 초과했습니다.(최대 5개)')

            # 3. 없으면 default_location 설정 
            default_location_flag = self.destination_dao.check_default_location_by_user(connection, data['user_id'])

            if not default_location_flag:
                data['default_location'] = 1
            else:
                data['default_location'] = 0

            # 4. 유저 생성
            return self.destination_dao.create_destination_dao(connection, data)

        except KeyError:
            raise KeyError('키값이 일치 하지 않습니다.')

    def delete_destination_service(self, connection, data):

        """ 배송지 삭제 서비스
        삭제한 배송지가 기본 배송지 였을 수도 있기때문에, 기본 배송지 값이 삭제되면
        남은 데이터의 최근 데이터를 기본 배송지로 설정해준다.

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
            2020-12-31(김기용): 로직에 간단한 설명 주석 삽입

        """
        try:
            # 1. 계정이 유저인지 확인 True/False
            if not data['permission_type_id'] == 3:
                    raise NotUser('유저가 아닙니다.')

            # 2. 삭제
            self.destination_dao.delete_destination_dao(connection, data)

            # 3. 기본 배송지 값이 지워졌을 수도 있으므로 기본값이 있는지 확인 True/False
            default_location_flag = self.destination_dao.check_default_location(connection, data)

            # 4. 기본 배송지가 삭제 되었다면 기본 배송지 자동 설정  
            if not default_location_flag:
                self. destination_dao.update_default_location_true(connection, data)


        except KeyError:
            raise KeyError('키값이 일치하지 않습니다.')

