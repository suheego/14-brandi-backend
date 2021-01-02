from flask import jsonify, g
from flask.views import MethodView

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.decorator import signin_decorator


class SenderView(MethodView):
    """ Presentation Layer

    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service : SenderService 클래스

    Author: 고수희

    History:
        2020-12-30(고수희): 초기 생성
    """
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @signin_decorator(True)
    def get(self):
        """ GET 메소드: 해당 유저가 사용한 가장 최신의 주문자 정보 조회

        user_id에 해당되는 주문 내역들을 조회해서, 가장 최근에 사용한 주문자 정보 사용

        Author: 고수희

        Returns: {
                    "name": "고수희",
                    "phone": "01021341234,
                    "email": "gosuhee@gmail.com"

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값
            403, {'message': 'key error',
            'errorMessage': 'customer_permission_denied'} : 사용자 권한이 없음

        History:
            2020-12-30(고수희): 초기 생성
            2021-01-02(고수희): decorator 수정
        """

        data = {
            "user_id": g.account_id,
            "user_permission": g.permission_type_id
        }

        try:
            connection = get_connection(self.database)
            sender_info = self.service.get_sender_info_service(connection, data)
            return jsonify({'message': 'success', 'result': sender_info})

        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
