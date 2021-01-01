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
from utils.rules import NumberRule, DecimalRule, EmailRule, PostalCodeRule, PhoneRule
from utils.decorator import signin_decorator


class StoreOrderView(MethodView):
    """ Presentation Layer

    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service: CartItemService 클래스

    Author: 고수희

    History:
        2020-12-30(고수희): 초기 생성
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @signin_decorator
    @validate_params(
        Param('cart_id', PATH, str)
    )
    def get(self, *args):
        """ GET 메소드: 해당 유저의 장바구니 상품 정보를 조회.

        cart_id에 해당되는 장바구니 상품을 테이블에서 조회 후 가져옴

        Args: args = ('account_id', 'cart_id')

        Author: 고수희

        Returns:
            return {
            "message": "success",
            "result": {"totalPrice"":9000,


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
            2020-12-30(고수희): 1차 수정 - 데코레이터 추가, 사용자 권한 체
        """
        data = {
            "cart_id": args[0],
            "user_id": g.account_id
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


class StoreOrderAddView(MethodView):
    """ Presentation Layer

    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service : CartItemService 클래스

    Author: 고수희

    History:
        2020-12-30(고수희): 초기 생성
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @signin_decorator
    @validate_params(
        Param('productId', JSON, str, rules=[NumberRule()]),
        Param('stockId', JSON, str, rules=[NumberRule()]),
        Param('quantity', JSON, str, rules=[NumberRule()]),
        Param('originalPrice', JSON, str, rules=[DecimalRule()]),
        Param('sale', JSON, str, rules=[DecimalRule()]),
        Param('discountedPrice', JSON, str, rules=[DecimalRule()]),
        Param('soldOut', JSON, bool),
        Param('senderName', JSON, str),
        Param('senderPhone', JSON, str, rules=[DecimalRule()]),
        Param('senderEmail', JSON, str, rules=[EmailRule()]),
        Param('recipientName', JSON, str, rules=[DecimalRule()]),
        Param('recipientPhone', JSON, str, rules=[PhoneRule()]),
        Param('recipientEmail', JSON, str, rules=[EmailRule()]),
        Param('address1', JSON, str),
        Param('address2', JSON, str),
        Param('postNumber', JSON, str, rules=[PostalCodeRule()]),
        Param('deliveryId', JSON, str, rules=[NumberRule()]),
        Param('deliveryMemo', JSON, str, required=False),
        Param('deliveryMemoDefault', JSON, str, rules=[NumberRule()])
    )
    def post(self, *args):
        """POST 메소드: 장바구니 상품 생성

        Args: args = ('account_id', 'product_id', 'stock_id', 'quantity', 'origin_price', 'sale', 'discounted_price')

        Author: 고수희

        Returns:
            200, {'message': 'success'} : 결제 성공

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값
            400, {'message': 'cart item create error',
            'errorMessage': 'cart_item_create_error'} : 결제 실패
            400, {'message': 'unable to close database',
            'errorMessage': 'unable_to_close_database'} : 커넥션 종료 실패
            403, {'message': 'customer permission denied',
            'errorMessage': 'customer_permission_denied'} : 사용자 권한이 아님
            500, {'message': 'internal server error',
            'errorMessage': format(e)}) : 서버 에러

        History:
            2020-12-30(고수희): 초기 생성
        """
        data = {
            'user_id': g.account_id,
            'product_id': args[0],
            'stock_id': args[1],
            'quantity': args[2],
            'original_price': args[3],
            'sale': args[4],
            'discounted_price': args[5],
            'sold_out': args[6],
            'sender_name': args[7],
            'sender_phone': args[8],
            'sender_email': args[9],
            'recipient_name': args[10],
            'recipient_phone': args[11],
            'recipient_email': args[12],
            'address1': args[13],
            'address2': args[14],
            'post_number': args[15],
            'delivery_memo_type_id': args[16],
            'delivery_content': args[17],
            'delivery_default': args[18]
        }
        print(data)
        try:
            connection = get_connection(self.database)
            cart_id = self.service.post_cart_item_service(connection, data)
            connection.commit()
            return {'message': 'success', 'result': {"cartId": cart_id}}, 201

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
