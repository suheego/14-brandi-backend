from flask import jsonify
from flask.views import MethodView
from flask_request_validator import (
    PATH,
    Param,
    JSON,
    validate_params
)

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import NumberRule, DecimalRule
from utils.decorator import signin_decorator


class SellerShopView(MethodView):
    """ Presentation Layer

    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service: SellerShopService 클래스

    Author: 고수희

    History:
        2021-01-01(고수희): 초기 생성
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('seller_id', PATH, str)
    )
    def get(self, *args):
        """ GET 메소드: 해당 셀러의 정보 출력

        account_id에 해당되는 셀러 정보를 테이블에서 조회 후 가져옴

        Args: args = ('account_id')

        Author: 고수희

        Returns:
            {
            "message": "success",
            "result": {
                "background_image": "https://img.freepik.com/free-psd/top-view-t-shirt-concept-mock-up_23-2148809114.jpg?size=626&ext=jpg&ga=GA1.2.1060993109.1605750477",
                "english_name": "i am seller_2",
                "id": 2,
                "name": "나는셀러2",
                "profile_image": "https://img.freepik.com/free-psd/logo-mockup-white-paper_1816-82.jpg?size=626&ext=jpg&ga=GA1.2.1060993109.1605750477"
                }
            }

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값
            400, {'message': 'seller does not exist error',
            'errorMessage': 'seller_does_not_exist'} : 셀러 정보 조회 실패
            400, {'message': 'unable to close database',
            'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error',
            'errorMessage': format(e)}) : 서버 에러

        History:
            2021-01-01(고수희): 초기 생성
        """
        data = {
            "account_id": args[0]
        }

        try:
            connection = get_connection(self.database)
            seller_info = self.service.get_seller_info_service(connection, data)
            return jsonify({'message': 'success', 'result': seller_info})

        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')