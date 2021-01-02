from flask import jsonify
from flask.views import MethodView
from flask_request_validator import (
    GET,
    PATH,
    Param,
    JSON,
    validate_params
)

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
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

    @signin_decorator(False)
    @validate_params(
        Param('seller_id', PATH, int)
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

        account_id = args[0]

        try:
            connection = get_connection(self.database)
            seller_info = self.service.get_seller_info_service(connection, account_id)
            return jsonify({'message': 'success', 'result': seller_info})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

class SellerShopSearchView(MethodView):
    """ Presentation Layer

    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service: SellerShopService 클래스

    Author: 고수희

    History:
        2021-01-02(고수희): 초기 생성
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @signin_decorator(False)
    @validate_params(
        Param('seller_id', PATH, int),
        Param('keyword', GET, str),
        Param('offset', GET, int, required=False, default=0),
        Param('limit', GET, int, required=False, default=30)
    )
    def get(self, *args):
        """ GET 메소드: 해당 셀러의 상품 검색 결과 출력

        keyword에 해당되는 셀러 정보를 테이블에서 조회 후 가져옴

        Args: args = ('seller_id', 'keyword', 'offset', 'limit')

        Author: 고수희

        Returns:
            {"message": "success",
            "result": [
            {
            "discount_rate": 0.1,
            "discounted_price": 9000.0,
            "image": "https://img.freepik.com/free-psd/simple-black-men-s-tee-mockup_53876-57893.jpg?size=338&ext=jpg&ga=GA1.2.1060993109.1605750477",
            "origin_price": 10000.0,
            "product_id": 7,
            "product_name": "성보의하루7",
            "product_sales_count": null,
            "seller_id": 4,
            "seller_name": "나는셀러4"
        },
        {
            "discount_rate": 0.1,
            "discounted_price": 9000.0,
            "image": "https://img.freepik.com/free-psd/simple-black-men-s-tee-mockup_53876-57893.jpg?size=338&ext=jpg&ga=GA1.2.1060993109.1605750477",
            "origin_price": 10000.0,
            "product_id": 5,
            "product_name": "성보의하루5",
            "product_sales_count": null,
            "seller_id": 4,
            "seller_name": "나는셀러4"
            }]}

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값
            400, {'message': 'seller does not exist error',
            'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error',
            'errorMessage': format(e)}) : 서버 에러

        History:
            2021-01-02(고수희): 초기 생성
        """

        data = {
            "seller_id": args[0],
            "keyword": "%"+args[1]+"%",
            "offset": args[2],
            "limit": args[3]
        }
        try:
            connection = get_connection(self.database)
            search_product_list = self.service.get_seller_product_search_service(connection, data)
            return jsonify({'message': 'success', 'result': search_product_list})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
