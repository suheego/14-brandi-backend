from flask import jsonify
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import NumberRule, GenderRule, AlphabeticRule
from flask_request_validator import (
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
        Param('cartId', JSON, str, rules=[NumberRule()]),
    )
    #login_decorator
    def get(self, user_id, *args):
        data = {
            'cart_id': args[0],
        }
        """GET 메소드: 해당 장바구니 상품 정보를 조회.

        cart_id 에 해당되는 상품을 테이블에서 조회 후 가져온다.

        Args: args = ('cart_id')

        Author: 고수희

        Returns:
            return {"message": "success", "result": [{"id": "1", "productId": "남자", "id": 12, "name": "홍길동"}]}

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'cart item not exist error', 'errorMessage': 'cart_items_does품_not_exist'}    : 장바구니 상품 조회 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-28(고수희): 초기 생성
        """

        try:
            connection = get_connection(self.database)
            items = self.service.get_cart_item_service(connection, data)
            return jsonify({'message': 'success', 'result': items})

        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

    @validate_params(
        Param('productId', JSON, str, rules=[NumberRule()]),
        Param('stockId', JSON, str, rules=[NumberRule()]),
        Param('quantity', JSON, str, rules=[NumberRule()]),
        Param('originPrice', JSON, str, rules=[NumberRule()]),
        Param('sale', JSON, str, rules=[NumberRule()]),
        Param('discountedPrice', JSON, str, rules=[NumberRule()])
    )
    #login_decorator
    def post(self, *args):
        data = {
            #'user_id' : user_id,
            'product_id': args[0],
            'stock_id': args[1],
            'quantity': args[2],
            'origin_price': args[3],
            'sale': args[4],
            'discounted_price': args[5],
        }
        """POST 메소드: 장바구니 상품 생성

        Args: args = ('product_id', 'stock_id', 'quantity', 'origin_price', 'sale', 'discounted_price')

        Author: 고수희

        Returns:
            200, {'message': 'success'}                                                             : 유저 생성 성공

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'cart item create error', 'errorMessage': 'user_create_error'}         : 장바구니 상품 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-28(고수희): 초기 생성
        """

        try:
            connection = get_connection(self.database)
            self.service.post_cart_item_service(connection, data)
            connection.commit()
            return {'message': 'success', "result": [{"id": "1"}, {"id": "2"}]}

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
