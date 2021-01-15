from flask import jsonify, g
from flask.views import MethodView
from flask_request_validator import (
    PATH,
    Param,
    JSON,
    validate_params
)

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import DecimalRule
from utils.decorator import signin_decorator


class CartItemView(MethodView):
    """ Presentation Layer

    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service: CartItemService 클래스

    Author: 고수희

    History:
        2020-12-28(고수희): 초기 생성
        2021-01-01(고수희): response 수정
        2020-01-02(고수희): decorator 수정
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @signin_decorator(True)
    @validate_params(
        Param('cart_id', PATH, int)
    )
    def get(self, *args):
        """ GET 메소드: 해당 유저의 장바구니 상품 정보를 조회.

        cart_id에 해당되는 장바구니 상품을 테이블에서 조회 후 가져옴

        Args: args = ('account_id', 'cart_id')

        Author: 고수희

        Returns:
            return
                    {
                        "message": "success",
                        "result": {
                            "cart_item": {
                                "color": "Black",
                                "discounted_price": 9000.0,
                                "id": 23,
                                "image_url": "https://img.freepik.com/free-psd/simple-black-men-s-tee-mockup_53876-57893.jpg?size=338&ext=jpg&ga=GA1.2.1060993109.1605750477",
                                "original_price": 14000.0,
                                "product_id": 1,
                                "product_name": "성보의하루1",
                                "quantity": "1",
                                "sale": 0.1,
                                "seller_name": "나는셀러9",
                                "size": "Free",
                                "soldout": false,
                                "stock_id": 1,
                                "total_price": 9000.0
                            }
                        }
                    }

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값
            400, {'message': 'cart item does not exist error',
            'errorMessage': 'cart_item_does_not_exist'} : 장바구니 상품 정보 조회 실패
            400, {'message': 'unable to close database',
            'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error',
            'errorMessage': format(e)}) : 서버 에러

        History:
            2020-12-28(고수희): 초기 생성
            2020-12-30(고수희): 1차 수정 - 데코레이터 추가, 사용자 권한 체크
            2020-01-02(고수희): decorator 수정
        """
        data = {
            "cart_id": args[0],
            "user_id": g.account_id,
            "user_permission": g.permission_type_id
        }

        try:
            connection = get_connection(self.database)
            cart_items = self.service.get_cart_item_service(connection, data)
            return jsonify({'message': 'success', 'result': cart_items})

        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class CartItemAddView(MethodView):
    """ Presentation Layer

    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service : CartItemService 클래스

    Author: 고수희

    History:
        2020-12-28(고수희): 초기 생성
        2020-01-02(고수희): decorator 수정
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @signin_decorator(True)
    @validate_params(
        Param('productId', JSON, int),
        Param('stockId', JSON, int),
        Param('quantity', JSON, int),
        Param('originalPrice', JSON, str, rules=[DecimalRule()]),
        Param('sale', JSON, str, rules=[DecimalRule()]),
        Param('discountedPrice', JSON, str, rules=[DecimalRule()])
    )
    def post(self, *args):
        """POST 메소드: 장바구니 상품 생성

        Args: args = ('account_id', 'product_id', 'stock_id', 'quantity', 'origin_price', 'sale', 'discounted_price')

        Author: 고수희

        Returns:
            200, {'message': 'success'} : 장바구니 상품 추가 성공

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값
            400, {'message': 'cart item create error',
            'errorMessage': 'cart_item_create_error'} : 장바구니 상품 추가 실패
            400, {'message': 'unable to close database',
            'errorMessage': 'unable_to_close_database'} : 커넥션 종료 실패
            403, {'message': 'customer permission denied',
            'errorMessage': 'customer_permission_denied'} : 사용자 권한이 아님
            500, {'message': 'internal server error',
            'errorMessage': format(e)}) : 서버 에러

        History:
            2020-12-28(고수희): 초기 생성
            2020-12-30(고수희): 1차 수정 - 데코레이터 추가, 사용자 권한 체크 추가
        """
        data = {
            'user_id': g.account_id,
            'user_permission': g.permission_type_id,
            'product_id': args[0],
            'stock_id': args[1],
            'quantity': args[2],
            'original_price': args[3],
            'sale': args[4],
            'discounted_price': args[5]
        }

        try:
            connection = get_connection(self.database)
            cart_id = self.service.post_cart_item_service(connection, data)
            connection.commit()
            return {'message': 'success', 'result': {"cart_id": cart_id}}, 201

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
