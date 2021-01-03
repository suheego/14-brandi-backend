from utils.custom_exceptions import CustomerPermissionDenied


class SenderService:
    """ Business Layer

        Attributes:
            orderer_dao: OrdererDao 클래스

        Author: 고수희

        History:
            2020-12-30(고수희): 초기 생성
    """

    def __init__(self, sender_dao):
        self.sender_dao = sender_dao

    def get_sender_info_service(self, connection, data):
        """ GET 메소드: 사용자의 주문자 정보 조회

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 고수희

        Returns:
            return (): 주문자 이름, 휴대폰 번호, 이메일 반환

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값
            400, {'message': 'unable to close database',
            'errorMessage': 'unable_to_close_database'} : 커넥션 종료 실패
            403, {'message': 'customer permission denied',
            'errorMessage': 'customer_permission_denied'} : 사용자 권한이 아님
            500, {'message': 'internal server error',
            'errorMessage': format(e)}) : 서버 에러
일
        History:
            2020-12-30(고수희): 초기 생성
        """
        try:
            # 사용자의 권한 체크
            permission_check = self.sender_dao.get_user_permission_check_dao(connection, data)
            if permission_check['permission_type_id'] != 3:
                raise CustomerPermissionDenied('customer_permission_denied')

            #주문 정보 조회
            return self.sender_dao.get_sender_info_dao(connection, data)

        except KeyError:
            raise KeyError('key_error')
