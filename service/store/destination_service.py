from utils.custom_exceptions import NotUser

class DestinationService:

    def __init__(self, destination_dao):
        self.destination_dao = destination_dao

    def get_destination_detail_by_user_service(self, connection, data):
        """ 유저 배송지 조회 서비스

        View에서 받은 connection 객체와 data를 model 계층으로 넘겨준다.

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

        View에서 받은 connection 객체와 data를 model 계층으로 넘겨준다.

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


            # 2. check_default_location 메서드를 통해 기본 배송지 설정 여부를 판단한다.
            default_location = self.destination_dao.check_default_location(connection, data['user_id'])

            # 리턴받은 튜플에 첫번째 인덱스에 접근
            if not default_location:
                data['default_location'] = 1
            else:
                for row in default_location:
                    if row[0] == 1:
                        data['default_location'] = 0
                        break
                    else:
                        data['default_location'] = 1

            return self.destination_dao.create_destination_dao(connection, data)
        except KeyError:
            raise KeyError('key_error')
