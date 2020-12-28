from flask import jsonify
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import NumberRule, GenderRule, AlphabeticRule, DecimalRule, ListInNumberRule
from flask_request_validator import (
    GET,
    Param,
    JSON,
    validate_params
)


class CartItemView(MethodView):
    """ Presentation Layer

    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service : CartItemService 클래스

    Author: 고수희

    History:
        2020-12-28(고수희): 초기 생성
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        # 결제를 시도하려는 장바구니 상품이 여러개일 수 있으므로 list로 받음
        Param('cartIds', GET, list, rules=[ListInNumberRule()])
    )
    #login_decorator
    def get(self, cartIds):
        """ GET 메소드: 해당 유저의 장바구니 정보를 조회.

        cartIds에 해당되는 상품을 테이블에서 조회 후 가져옴

        Args: args = ('cart_id')

        Author: 고수희

        Returns:
            return {
            "message": "success",
            "result": [{"id":"3",
                        "product_id": "3",
                        "stock_id": "41",
                        "quantity": "1",
                        "sale":"0.10",
                        "origin_price":"10000",
                        "discounted_price":"9000"
                        }]}

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
        """

        data = {
            'cart_id': cartIds
            #'user_id': user_id
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

    @validate_params(
        Param('userId', JSON, str, rules=[NumberRule()]),
        Param('productId', JSON, str, rules=[NumberRule()]),
        Param('stockId', JSON, str, rules=[NumberRule()]),
        Param('quantity', JSON, str, rules=[NumberRule()]),
        Param('originalPrice', JSON, str, rules=[DecimalRule()]),
        Param('sale', JSON, str, rules=[DecimalRule()]),
        Param('discountedPrice', JSON, str, rules=[DecimalRule()])
    )
    #login_decorator
    def post(self, *args):
        data = {
            'user_id': args[0],
            'product_id': args[1],
            'stock_id': args[2],
            'quantity': args[3],
            'original_price': args[4],
            'sale': args[5],
            'discounted_price': args[6]
        }

        """POST 메소드: 장바구니 상품 생성 

        Args: args = ('product_id', 'stock_id', 'quantity', 'origin_price', 'sale', 'discounted_price')

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
        """

        try:
            connection = get_connection(self.database)
            cart_items = self.service.post_cart_item_service(connection, data)
            connection.commit()
            return {'message': 'success', 'result': {"id": cart_items}}

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
