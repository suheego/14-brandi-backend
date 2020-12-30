from flask import jsonify
from flask.views import MethodView

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import NumberRule, GenderRule, AlphabeticRule, OrderStatusRule

from flask_request_validator import (
    Param,
    JSON,
    validate_params,
    GET
)


class OrderView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database
        print("hello world")

    @validate_params(
        Param('account', GET, int, required=True),
        Param('status', GET, int, required=True, rules=[OrderStatusRule()]),
        Param('number', GET, str, required=False),
        Param('detail_number', GET, str, required=False),
        Param('sender_name', GET, str, required=False),
        Param('sender_phone', GET, str, required=False),
        Param('seller_name', GET, str, required=False),
        Param('product_name', GET, str, required=False),
        Param('start_date', GET, str, required=False),
        Param('end_date', GET, str, required=False),
        Param('seller_attributes', JSON, list, required=False),
        Param('order_by', GET, str, required=True),
        Param('page', GET, int, required=True),
        Param('length', GET, int, required=True)
    )
    def get(self, *args):
        data = {
            'account': args[0],
            'status': args[1],
            'number': args[2],
            'detail_number': args[3],
            'sender_name': args[4],
            'sender_phone': args[5],
            'seller_name': args[6],
            'product_name': args[7],
            'start_date': args[8],
            'end_date': args[9],
            'seller_attributes': args[10],
            'order_by': args[11],
            'page': args[12],
            'length': args[13]
        }

        """GET 메소드: 주문 정보를 조회.

        account_id 에 해당되는 유저를 테이블에서 조회 후 가져온다.

        Args: args = ('account_id', 'status', 'number', 'detail_number', 'sender_name', 'sender_phone',
        'seller_name', 'product_name')

        Author: 김민서

        Returns:
            return {"message": "success", "result": [{"age": "18", "gender": "남자", "id": 12, "name": "홍길동"}]}

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'user does not exist error', 'errorMessage': 'user_does_not_exist'}    : 유저 정보 조회 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-20-20(홍길동): 초기 생성
            2020-20-21(홍길동): 1차 수정
            2020-20-22(홍길동): 2차 수정
        """

        try:
            connection = get_connection(self.database)
            contexts = self.service.get_prepare_product_service(connection, data)
            result = []

            for context in contexts:
                context["option_extra_cost"] = str(context["option_extra_cost"])
                context["total_price"] = str(context["total_price"])
                result.append(context)

            return jsonify({'message': 'success', 'result': result})
        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

    @validate_params(
        Param('order_status_id', JSON, int)
    )
    def patch(self, *args):
        order_status_id = args[0]

        try:
            connection = get_connection(self.database)
            self.service.get_order_status_service(connection, order_status_id)
            return jsonify({'message': 'success'})
        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
